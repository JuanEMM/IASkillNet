# Límites de la métrica de evaluación


## Qué mide

Compara las palabras de la respuesta del modelo con las de una
referencia y cuenta cuántas coinciden, incluyendo repeticiones
(precisión, cobertura y F1).


## Modos de falla conocidos

- Los sinónimos y las palabras escritas distinto puntúan bajo. En
  la pregunta de la lista, la respuesta dice "mutable" y la
  referencia "modificable", y no cuenta. Pasa igual con "creó" y
  "creado", o con "programacion" sin tilde frente a "programación".
- El formato JSON de la respuesta baja la precisión. Las claves
  (`dateInput`, `items`, `atributo`, `valor`, `calidad`) cuentan
  como palabras. En "¿Cuándo se creó Python?" el 1991 está bien,
  pero la precisión es 0.14 porque solo 2 de 14 palabras coinciden.
- Algunas coincidencias no vienen de la respuesta en sí. En el
  caso de la fecha, `dateInput` repite la pregunta y de ahí sale la
  palabra "python". En el caso de la lista, una de las dos
  coincidencias es la "y".
- Un dato incorrecto puede puntuar alto si el resto de la oración
  coincide. No pasó en mi muestra, pero por cómo se calcula,
  "Python fue creado en 1995" contra "Python fue creado en 1991"
  da F1 de 0.80.
- Una negación que falta casi no baja el puntaje, aunque cambie el
  significado. Tampoco pasó en la muestra; "Python no es un
  lenguaje de programación interpretado" daría F1 cercano a 0.93.
- Las respuestas traen un `dateInput` con fecha (2023-10-25) que
  nadie pidió. La métrica no lo detecta como un problema.


## Muestra revisada

3 casos, que son todos los de `revision_manual.json`. Como son tan
pocos no pude elegir los mejores y los peores. Los F1 fueron 0.25,
0.21 y 0.09. Sirve para ver ejemplos de las fallas, pero no para
saber qué tan seguido ocurren.


## Recomendación de uso

No confiar en el valor del F1 por sí solo: en la muestra, las
respuestas más o menos correctas sacaron entre 0.09 y 0.25. Usarlo
solo para comparar versiones del cliente entre sí, siempre que el
modelo responda con el mismo formato. Si responde en JSON, conviene
sacar primero el campo `valor` y medir solo ese texto. Revisar a
mano cualquier respuesta con fechas, cifras, nombres propios o
negaciones.
