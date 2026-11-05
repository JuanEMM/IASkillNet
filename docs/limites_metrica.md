# Límites de la métrica de evaluación


## Qué mide

Coincidencia de palabras entre una respuesta generada y una
referencia, contando repeticiones (precisión, cobertura, F1). El
texto se pasa a minúsculas, se le quita la puntuación y se separa
por espacios; no se quitan tildes ni palabras vacías ("de", "y",
"en").


## Modos de falla conocidos

- Sinónimos, paráfrasis y variantes de escritura puntúan bajo. En
  "¿Qué es una lista en Python?" la respuesta dice "mutable" y la
  referencia "modificable": no cuenta como coincidencia. Lo mismo
  pasa con "creó" frente a "creado", y con "programacion" (sin
  tilde, en la respuesta) frente a "programación" (en la
  referencia).
- Una respuesta correcta puede puntuar muy bajo si el modelo la
  entrega con formato extra. Las 3 respuestas revisadas son JSON
  (`dateInput`, `items`, `atributo`, `valor`, `calidad`). Esas
  claves y números cuentan como palabras de la respuesta y
  hunden la precisión: en "¿Cuándo se creó Python?" el dato
  correcto (1991) aparece, pero la precisión es 0.14 (2 de 14
  palabras).
- Las coincidencias pueden venir de palabras vacías o del eco de
  la pregunta, no de la respuesta. En "¿Cuándo se creó Python?",
  `dateInput` repite la pregunta y de ahí sale la coincidencia
  "python"; en "¿Qué es una lista en Python?", una de las 2
  coincidencias es la "y" de "mutable y ordenada".
- Datos incorrectos (fechas, cifras) pueden puntuar alto si el
  resto de la oración coincide. No ocurrió en la muestra; se
  deduce del cálculo: "Python fue creado en 1995." contra la
  referencia "Python fue creado en 1991." da F1 = 0.80.
- Negaciones ausentes casi no bajan el puntaje, aunque inviertan
  el significado. Tampoco ocurrió en la muestra; por el mismo
  cálculo, "Python no es un lenguaje de programación
  interpretado." contra la referencia da F1 ≈ 0.93.
- Se detectó un dato inventado que la métrica no ve: las
  respuestas incluyen `"dateInput": "2023-10-25"` sin que la
  consulta pida fecha alguna.


## Muestra revisada

3 casos, que son todos los de `revision_manual.json`. No hubo
selección por mayor y menor F1 porque no hay más casos. Cada caso
tiene una sola referencia de una oración. F1 de los casos: 0.25,
0.21 y 0.09. Con 3 casos las conclusiones son preliminares: sirven
para ilustrar los modos de falla, no para estimar su frecuencia.


## Recomendación de uso

No confiar en el valor absoluto: en la muestra, respuestas en
esencia correctas puntúan entre 0.09 y 0.25. Usar F1 solo para
comparar entre versiones del cliente, y únicamente si el formato
de salida del modelo es el mismo en ambas. Si la salida es JSON,
conviene extraer primero el campo `valor` y evaluar solo ese
texto. Revisar siempre a mano cualquier respuesta con fechas,
cifras, nombres propios o negaciones.
