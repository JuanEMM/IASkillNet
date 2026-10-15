# Decisión de arquitectura: elección de modelo
  
 ## Modelo elegido
  Modelo de gemini, para la funcionalidad principal
 ## Diagrama de arquitectura
  Diagramna en Docs/diagrama_arquitectura.png, detallado
 ## Comparación de candidatos

Misma pregunta para ambos candidatos, 4 intentos cada uno. Fuentes: `resultado_Gemini2-5.md` y `resultado_OpenRouter.md`.

Latencia y costo

| | Gemini 2.5 Flash | OpenRouter(Grok 4.7) |
|---|---|---|
| Intento 1 | 21.94 s | 15.87 s |
| Intento 2 | 19.72 s | 17.56 s |
| Intento 3 | 20.65 s | 25.49 s |
| Intento 4 | 17.59 s | 35.33 s |
| **Latencia promedio** | **19.97 s** | **23.56 s** |
| **Costo de la última petición** | **USD 0.0081** | **USD 0.0148** |

- Gemini es ~18 % más rápido en promedio y más estable (17.6 a 21.9 s). OpenRouter varía de 15.9 a 35.3 s.
- OpenRouter costó ~83 % más por petición que Gemini.

Calidad de la respuesta

Gemini responde las tres partes de la pregunta (fecha, clima y limitaciones) de forma ordenada, aunque genérica. OpenRouter es más específica y útil en las limitaciones, pero no entrega la fecha ni el clima.

 ## Justificación
  Por respuesta más ordenada y limitaciones, se usará Gemini. El ejercicio se realizó con Gemini 2.5, pero para el proyecto se usará la versión 3.8, que es más actualizada y mejor; además, los tiempos son mejores (no se utlizo porque esta presentado problema por posible actualización).
 ## Alternativa descartada y por qué
  Se descartó OpenRouter(Grok 4.7) por el hecho de que no pudo confirmar su fecha de actualización, además de ser un poco más lento, aunque sus respuestas fueron más precisas y no tan genéricas como Gemini. Se limitaba mucho (se nego a dar fecha y clima), ademas de ser mas cara.