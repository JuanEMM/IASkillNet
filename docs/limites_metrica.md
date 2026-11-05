# Límites de la métrica de evaluación


## Qué mide

Compara las palabras de la respuesta del modelo con las de una
referencia y cuenta cuántas coinciden, incluyendo repeticiones
(precisión, cobertura y F1). Pasa todo a minúsculas y quita la
puntuación, pero no quita tildes ni palabras como "de" o "el".


## Modos de falla conocidos

- Una respuesta correcta puede sacar casi cero si usa otras
  palabras. En "¿Cuánto cuesta un flete?" el modelo responde
  "variable" y la referencia dice "depende de la distancia, el
  peso...": es casi lo mismo y el F1 es 0.0. Pasa igual con
  "mercaderias" frente a "mercancías" en la guía de despacho.
- El formato JSON ensucia el puntaje. Las claves y la fecha cuentan
  como palabras, y los nombres con guion bajo, como
  `peso_maximo_permitido`, quedan como una sola palabra, así que
  "peso" no coincide aunque la respuesta hable de peso. Además, si
  el modelo agrega ejemplos o requisitos, baja la precisión: en
  "carga sobredimensionada" la cobertura es 0.81 pero la precisión
  solo 0.18.
- Una cifra distinta casi no baja el puntaje. En "¿Cuántas
  toneladas puede llevar un camión de 2 ejes o más?" la referencia
  dice 45 y el modelo da 15, 23 a 26 y 31 según los ejes. Solo
  coinciden "hasta" y "toneladas" (F1 0.105), y el número pesa lo
  mismo que cualquier otra palabra.
- Una respuesta que dice lo contrario puede coincidir en palabras.
  En "¿Qué hacer si un neumático se calienta mucho en ruta?" la
  referencia (falsa) dice echar agua fría y el modelo dice evitar
  arrojar agua fría: coinciden "agua" y "fría". En "¿Cada cuánto se
  debe revisar la presión?" el modelo dice "una vez al mes" y la
  referencia "una vez al año", y saca 0.27, más que la tara
  (0.23), que estaba bien. Estos dos casos están fuera de la
  muestra de 10, pero se ven en los 20 resultados.
- Con una referencia falsa no se sabe quién tiene la razón. En
  "¿Con el neumático frío o caliente se mide la presión?" el modelo
  respondió bien ("frio") y sacó 0.0, y en "¿Un camión puede
  superar el peso máximo si la carga está bien amarrada?" respondió
  "no" y también sacó 0.0. Si hubiera repetido el error de la
  referencia, habría sacado un puntaje alto. La métrica mide
  parecido, no si algo es verdad.
- En las preguntas ambiguas el modelo da un valor concreto en vez
  de decir "depende", y no se puede saber si eso está mal. En "¿Cuál
  es la mejor ruta de entrega?" responde "Avenida Central", que se
  inventó, y en el combustible da "30 a 40 litros cada 100 km". Las
  dos sacan 0.0, pero la métrica no distingue entre inventar y dar
  una respuesta razonable.
- El modelo agrega un `dateInput` con una fecha (2023-10-24, 25 o 27)
  que nunca pedimos, y la métrica no lo marca.


## Muestra revisada

10 casos de 20: los 5 con menor F1 y los 5 con mayor F1. Los 20
casos son 8 certeras, 7 ambiguas y 5 con referencia falsa. El
promedio de F1 de los 20 fue 0.15.

- Menor F1 (los 5 con 0.0): mejor ruta, combustible, flete,
  frío o caliente, y superar el peso máximo. Son 3 ambiguas y 2
  falsas.
- Mayor F1: trazabilidad (0.52), peso bruto (0.31), guía de
  despacho (0.30), carga sobredimensionada (0.30) y tacógrafo
  (0.28). Son las 5 certeras.

Incluso la mejor respuesta sacó solo 0.52, y las demás buenas
quedaron cerca de 0.3.


## Recomendación de uso

No confiar en el número solo: con respuestas buenas el F1 anda
entre 0.2 y 0.5, así que el valor absoluto no dice si algo está
bien. Usarlo solo para comparar versiones del cliente entre sí, y
siempre que el modelo responda en el mismo formato. Antes de medir
conviene sacar el campo `valor` del JSON, cambiar los guiones bajos
por espacios y quitar las tildes. No sirve para detectar
respuestas falsas ni para evaluar preguntas ambiguas. Revisar a
mano cualquier respuesta con cifras, sí o no, negaciones y las
preguntas de seguridad (neumáticos, peso máximo).
