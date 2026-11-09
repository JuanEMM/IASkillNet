import json
from datetime import datetime, timezone
from pathlib import Path

# trazas_agente.jsonl vive en la raíz del proyecto
# (un nivel arriba de src/), sin importar desde qué
# carpeta se ejecute el script.
ARCHIVO_TRAZAS = (
    Path(__file__).resolve().parent.parent
    / "trazas_agente.jsonl"
)

def registrar_traza(
    session_id: str,
    entrada: str,
    resultado: dict,
) -> None:
    """Guarda una interacción del agente como una
    línea JSON en trazas_agente.jsonl: qué se
    preguntó, qué herramientas se usaron y con qué
    argumentos, y la respuesta final. Si "resultado"
    no trae "intermediate_steps" (por ejemplo, con
    return_intermediate_steps=False), acciones queda
    como una lista vacía en vez de fallar."""

    registro = {
        "timestamp": datetime.now(timezone.utc)
            .isoformat(),
        "session_id": session_id,
        "entrada": entrada,
        "acciones": [
            {
                "herramienta": accion.tool,
                "argumentos": accion.tool_input,
                "observacion": observacion,
            }
            for accion, observacion in resultado.get(
                "intermediate_steps", [])
        ],
        "respuesta_final": resultado["output"]
    }

    with open(
        ARCHIVO_TRAZAS, "a", encoding="utf-8"
    ) as archivo:
        archivo.write(
            json.dumps(registro, ensure_ascii=False)
            + "\n"
        )

def marcar_repeticiones_sospechosas(
    archivo: str | Path = ARCHIVO_TRAZAS,
) -> None:
    """Recorre un archivo de trazas y marca las
    sesiones donde la misma herramienta se invocó
    varias veces seguidas: un candidato a revisar a
    mano, no una conclusión definitiva."""
    try:
        with open(archivo, encoding="utf-8") as f:
            registros = [
                json.loads(linea) for linea in f
            ]
    except FileNotFoundError:
        print(
            f"No se encontró '{archivo}'. Corre "
            "registrar_traza al menos una vez antes "
            "de revisar repeticiones."
        )
        return

    for registro in registros:
        herramientas = [
            a["herramienta"]
            for a in registro.get("acciones", [])
        ]

        for i in range(1, len(herramientas)):
            if herramientas[i] == herramientas[i - 1]:
                print(
                    f"Revisar: {registro['session_id']} usó "
                    f"'{herramientas[i]}' dos veces seguidas"
                )
                break


if __name__ == "__main__":
    marcar_repeticiones_sospechosas()