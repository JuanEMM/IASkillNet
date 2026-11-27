# Registro de pruebas de la API
Fecha: 2026-11-27
Servicio probado: http://127.0.0.1:8000 (cliente: httpx2)
Resultado: 17 de 17 casos cumplidos

| Caso | Descripción | Petición | Esperado | Obtenido | Resultado |
|---|---|---|---|---|---|
| V-01 | CA-04/CA-05: consulta por patente con su fuente | POST /consultas {"pregunta": "cuando ingreso el camion B... | 200 | 200 | PASA |
| V-02 | CA-06: consulta que los documentos no cubren | POST /consultas {"pregunta": "cual es el horario del cas... | 200 | 200 | PASA |
| V-03 | ingreso de hoy de una patente existente | GET /ingresos/BXKL45 | 200 | 200 | PASA |
| V-04 | comprobacion de salud | GET /salud | 200 | 200 | PASA |
| V-05 | CA-01: extraccion de una guia valida | POST /extracciones {"texto": "Guia de despacho N 100231. Re... | 200 | 200 | PASA |
| I-01 | falta el campo pregunta | POST /consultas {} | 422 | 422 | PASA |
| I-02 | pregunta vacia | POST /consultas {"pregunta": ""} | 422 | 422 | PASA |
| I-03 | pregunta solo con espacios | POST /consultas {"pregunta": "   "} | 422 | 422 | PASA |
| I-04 | pregunta de 600 caracteres | POST /consultas {"pregunta": "aaaaaaaaaaaaaaaaaaaaaaaaaa... | 422 | 422 | PASA |
| I-05 | pregunta con tipo incorrecto | POST /consultas {"pregunta": 123} | 422 | 422 | PASA |
| I-06 | cuerpo que no es JSON valido | POST /consultas {"pregunta":  | 422 | 422 | PASA |
| I-07 | patente mal formada | GET /ingresos/ABC | 422 | 422 | PASA |
| I-08 | patente sin ingreso hoy | GET /ingresos/ZZZZ99 | 404 | 404 | PASA |
| I-09 | metodo no permitido | GET /consultas | 405 | 405 | PASA |
| I-10 | ruta que no existe | GET /ruta-inexistente | 404 | 404 | PASA |
| I-11 | guia demasiado corta | POST /extracciones {"texto": "RUT 12.345.678-5"} | 422 | 422 | PASA |
| I-12 | guia de 2001 caracteres | POST /extracciones {"texto": "ggggggggggggggggggggggggggggg... | 422 | 422 | PASA |
