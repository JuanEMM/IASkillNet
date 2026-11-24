"""Genera la evidencia del Gate 2: corre el servicio RAG y guarda el resultado en un JSON.

Uso (mejor desde una terminal, para que la aprobacion final la escriba una persona):
    python src/generar_evidencia.py
    python src/generar_evidencia.py --salida docs/otra_evidencia.json

Necesita GEMINI_API_KEY en el .env y conexion. No modifica servicio_rag.py ni ningun otro archivo:
solo escribe el JSON de salida (por defecto docs/evidencia_gate2.json).
"""
import argparse
import json
import os
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
os.chdir(RAIZ)  # el indice (indice_gate2/) es relativo a la carpeta de ejecucion: siempre el de la raiz

import servicio_rag as s  # noqa: E402
from langgraph.types import Command  # noqa: E402

# Preguntas del proyecto: la principal es la de main() en servicio_rag.py
CONSULTAS = [
    ("principal", "que camiones ingresaron el dia de hoy"),
    ("sin_salida", "que camiones de hoy aun no tienen salida"),
    ("por_patente", "cuando ingreso el camion BXKL45"),
    ("procedimiento", "que pasa si la calidad de un dato es menor a 4"),
]


def analizar(pregunta, r):
    """Devuelve (respuesta como objeto, verificaciones) a partir de lo que devolvio el servicio."""
    try:
        datos = json.loads(r["respuesta"])
        items = datos["items"]
        valido = isinstance(items, list) and "dateInput" in datos
    except (ValueError, KeyError, TypeError):
        return r["respuesta"], {"json_valido": False}
    return datos, {
        "json_valido": valido,
        "citas_dentro_de_lo_recuperado": all(i.get("fuente") in r["fuentes"] for i in items),
        "calidad_entre_1_y_5": all(isinstance(i.get("calidad"), int) and 1 <= i["calidad"] <= 5 for i in items),
        "auditoria_sin_pregunta_cruda": pregunta not in json.dumps(r["auditoria"], ensure_ascii=False),
    }


def tokens(auditoria):
    for evento in auditoria:
        if evento["evento"] == "consumo_llm":
            return evento.get("input_tokens") or 0, evento.get("output_tokens") or 0
    return 0, 0


def main():
    parser = argparse.ArgumentParser(description="Genera la evidencia del Gate 2 en un JSON.")
    parser.add_argument("--salida", default=str(RAIZ / "docs" / "evidencia_gate2.json"),
                        help="archivo JSON de salida (por defecto docs/evidencia_gate2.json)")
    args = parser.parse_args()

    vectorstore, estado_indice = s.cargar_indice()
    evidencia = {
        "generado": datetime.now().astimezone().isoformat(timespec="seconds"),
        "modelo": getattr(s.llm, "model", None),
        "embeddings": getattr(s.embeddings, "model", None),
        "indice": {"directorio": s.INDICE_DIR, "estado": estado_indice,
                   "documentos": len(vectorstore.get()["ids"])},
        "huella_prompt": s.HUELLA_PROMPT,
        "consultas": [],
    }

    # ---- consultas: se mide la latencia total de cada una (embedding, busqueda, generacion y reintentos)
    for nombre, pregunta in CONSULTAS:
        print(f"\n=== {nombre}: {pregunta}", flush=True)
        registro = {"nombre": nombre, "pregunta": pregunta}
        inicio = time.perf_counter()
        try:
            r = s.responder(pregunta, vectorstore, estado_indice)
        except Exception as error:  # noqa: BLE001  el fallo queda en la evidencia en vez de ocultarse
            registro.update(latencia_s=round(time.perf_counter() - inicio, 2),
                            error=f"{type(error).__name__}: {error}"[:300])
            print("FALLO:", registro["error"], flush=True)
        else:
            respuesta, verificaciones = analizar(pregunta, r)
            registro.update(trace_id=r["trace_id"], latencia_s=round(time.perf_counter() - inicio, 2),
                            respuesta=respuesta, fuentes_recuperadas=r["fuentes"],
                            auditoria=r["auditoria"], verificaciones=verificaciones)
        evidencia["consultas"].append(registro)

    # ---- supervision humana: el grafo se pausa y la decision la escribe una persona en la terminal
    print("\n=== punto de supervision humana", flush=True)
    config = {"configurable": {"thread_id": "evidencia-" + uuid.uuid4().hex[:8]}}
    pausado = s.app_despliegue.invoke({"huella_nueva": s.HUELLA_PROMPT, "aprobado": False}, config=config)
    if "__interrupt__" not in pausado:
        evidencia["supervision"] = {"error": "el grafo no se detuvo en el punto de supervision"}
    else:
        pendiente = pausado["__interrupt__"][0].value
        print("pausado, pendiente:", pendiente, flush=True)
        origen = ("terminal interactiva" if sys.stdin.isatty()
                  else "entrada redirigida (no es una persona escribiendo en una terminal)")
        aprobado = s.pedir_decision(f"Aprobar la version {s.HUELLA_PROMPT} del prompt en produccion? (s/n): ")
        final = s.app_despliegue.invoke(Command(resume=aprobado), config=config)
        evidencia["supervision"] = {
            "pausa": pendiente,
            "decision": "aprobada" if final.get("aprobado") else "rechazada",
            "origen_de_la_decision": origen,
            "registro_aprobaciones": list(s.registro_aprobaciones),
        }

    # ---- resumen
    ok = [c for c in evidencia["consultas"] if "error" not in c]
    latencias = [c["latencia_s"] for c in ok]
    entrada_salida = [tokens(c["auditoria"]) for c in ok]
    evidencia["resumen"] = {
        "consultas": len(evidencia["consultas"]),
        "con_error": len(evidencia["consultas"]) - len(ok),
        "verificaciones_ok": bool(ok) and len(ok) == len(evidencia["consultas"])
                             and all(all(c["verificaciones"].values()) for c in ok),
        "latencia_promedio_s": round(sum(latencias) / len(latencias), 2) if latencias else None,
        "latencia_maxima_s": max(latencias) if latencias else None,
        "tokens_entrada_total": sum(e for e, _ in entrada_salida),
        "tokens_salida_total": sum(o for _, o in entrada_salida),
    }

    salida = Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(json.dumps(evidencia, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nEvidencia guardada en {salida}")
    print(json.dumps(evidencia["resumen"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
