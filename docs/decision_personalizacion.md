# Decision de personalizacion

## 1. El proble
El extractor de datos de guías de transporte (chofer, RUT, patente, número de guía) devuelve JSON con la estructura correcta, pero los nombres de los atributos dentro de `items` no son consistentes entre respuestas (por ejemplo "rut" en una y "RUT del chofer" en otra). Esto impide cruzar de forma automática cada camión que ingresa a planta con su guía en el control de ingreso y salida. De 20 respuestas revisadas con una lista fija de atributos, [TU DATO: X] no la cumplen.

## 2. Resultado del metodo de decision
- PEFT: 5 puntos
- RAG: 2 puntos
- Fine-tuning completo: 1 punto

No hay empate: PEFT gana con claridad. Respondí True en formato (X de 20 respuestas fallan), presupuesto limitado y múltiples variantes; y False en información que cambia (el extractor no consulta documentos) y dataset grande (0 de 200 ejemplos etiquetados).

## 3. Tecnica elegida y por que
Elijo PEFT. Al modelo no le falta información, le falta consistencia en la salida, por eso descarto RAG. Descarto el fine-tuning completo porque no tengo los 200 ejemplos etiquetados que justifican reentrenar todos los parámetros, y es la opción más cara en datos, cómputo y tiempo. Además necesito [TU DATO: N] formatos de guía distintos, y con PEFT cada variante se resuelve con un adapter pequeño en vez de un modelo completo. Antes de entrenar probaré restringir `atributo` con un `enum` en el schema, como ya hice con `categoria` en `clasificar_incidencia`: si con eso las fallas bajan de 3 sobre 20, no haría falta personalizar.

## 4. Que necesitarias para ejecutarla
- Ejemplos etiquetados hoy: 0 guías reales (los 8 ejemplos de `laboratorio_dataset.py` son del curso y no sirven para este caso). Necesito 200, así que faltan 200.
- Tiempo de etiquetado: 200 ejemplos a 5 minutos cada uno son 1.000 minutos, unas 17 horas.
- Reparto: con [TU DATO: N] formatos de guía, al menos 30 ejemplos por formato.
- Calidad: revisar 20 ejemplos al azar y confirmar que ninguno tenga etiquetas contradictorias.
- Presupuesto: puedo pagar como máximo [TU DATO: N] intentos de entrenamiento.
- Corpus para indexar: ninguno, porque no uso RAG.
dos que faltan] que faltan]