# Revisión del alcance
Revisor: Claude, asistente de IA (revisión externa con la pauta de cinco criterios)
Fecha: 2026-11-27

- Hallazgo 1 (criterio 3): La sección 3 dice que la extracción de la guía se orquesta con LangChain, pero el componente que se reutiliza, `src/consumir_gemini.py`, llama a la API con `requests` y un `timeout` de 10 s, menor que los 30 s de RNF-01 y que los ~20 s medidos en `docs/decision-arquitectura.md`.
  Decisión: aceptado. Cambio: la extracción usa el prompt y el schema de `consumir_gemini.py` con el cliente LangChain y los reintentos de `servicio_rag.py`; se precisó en la sección 3 y en la funcionalidad RF-01 de `src/presupuesto/presupuesto_alcance.py`.

- Hallazgo 2 (criterio 4): CA-05 no pasaba la prueba ciega: exigía la fuente `ingreso-0007` y la hora 07:40, pero no decía de dónde salen esos datos ni que son del día de hoy.
  Decisión: aceptado. Cambio: CA-05 ahora indica que es el ingreso de hoy del camión BXKL45 en `INGRESOS_EJEMPLO` de `src/servicio_rag.py`, que el índice rearma cada día.

- Hallazgo 3 (criterio 2): RNF-01 (extracción en menos de 30 segundos) es el único umbral que no sale de una medición del proyecto; los demás se apoyan en el Gate 2.
  Decisión: aplazado. Se vuelve a evaluar al terminar H4, midiendo la extracción con las 10 guías de prueba.

Acierto: los RNF y sus criterios reutilizan cifras medidas en el Gate 2 (consultas de 1,5 a 2,8 s, listados de 41 a 46 s e índice de 27 documentos), y cada hito corresponde a una línea del informe de presupuesto, así que no hay que reinterpretar nada.
