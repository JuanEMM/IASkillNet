import json
from pathlib import Path

RUTA_RESULTADOS = Path(__file__).resolve().parent.parent / "resultados_metricas.json"

with open(RUTA_RESULTADOS, encoding="utf-8") as f:
    resultados = json.load(f)


def resumir_metricas(resultados):

    if not resultados:
        return {
            "precision_promedio": 0,
            "cobertura_promedio": 0,
            "f1_promedio": 0,
        }

    n = len(resultados)

    return {
        "precision_promedio": sum(
            r["precision"] for r in resultados
        ) / n,

        "cobertura_promedio": sum(
            r["cobertura"] for r in resultados
        ) / n,

        "f1_promedio": sum(r["f1"] for r in resultados) / n,
    }
print(resumir_metricas(resultados))

peores_casos = sorted(resultados, key=lambda r: r["f1"])

muestra_para_revisar = peores_casos[:5] + peores_casos[-5:]


for caso in muestra_para_revisar:

    print(caso["consulta"], caso["f1"])