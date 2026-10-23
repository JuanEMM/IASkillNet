"""Banco de prompts de la miniaplicación.

BANCO_DE_PROMPTS es una lista de diccionarios; cada uno describe una tarea que
se le pide al modelo y tiene estas claves:
    nombre: identificador del prompt.
    system_instruction: lo que se le explica al modelo sobre su tarea.
    ejemplo_usuario: texto de muestra para probarlo.
    claves_esperadas: claves que debe traer la respuesta para darla por válida.
    response_schema: esquema JSON que se le exige al modelo.

Prompts que hay hoy:
    obtener_datos_guia: saca chofer, RUT, número de guía, remitente, destinatario
        y dirección de entrega.
    obtener_datos_carga: saca patente, tipo de carga, peso, bultos, origen y destino.
    clasificar_incidencia: clasifica un problema en ruta (categoría, severidad de
        1 a 5, resumen y si necesita acción inmediata).

La usa prompts/test_consistencia.py. Para agregar uno basta con sumar otro
diccionario; claves_esperadas debería coincidir con el "required" de su esquema.
"""
BANCO_DE_PROMPTS = [
	{
    	"nombre": "obtener_datos_guia",
    	"system_instruction": (
        	"eres un asistente de inteligencia artificial que ayuda a los transportistas a extraer información de guías de transporte. Tu tarea es leer el texto proporcionado "
            "por el conductor y extraer los datos relevantes de la guía, nombre del chofer, su rut, el número de guía, el nombre del remitente, el nombre del destinatario, la dirección de entrega y cualquier otra información importante. Devuelve los datos en formato JSON  dentro de items con las claves "
            "'atributo' ,'valor' y 'calidad' (del 1 al 5 , indica la calidad del dato entregado) , y guardar la fecha de ejecucion de la peticion dentro de dateInput."
    	),
    	"ejemplo_usuario": "mi nombre es juan perez y mi numero de guia es 123456789, con fecha 1000/10/2029, el remitente es juan perez y el destinatario es maria lopez, la direccion de entrega es calle falsa 123, ciudad de mexico",
    	"claves_esperadas": ["dateInput", "items"],
    	"response_schema": {
            "type": "object",
            "properties": {
                "dateInput": {"type": "string"},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "atributo": {"type": "string"},
                            "valor": {"type": "string"},
                            "calidad": {"type": "number"}
                        },
                        "required": ["atributo", "valor", "calidad"]
                    }
                }
            },
            "required": ["dateInput", "items"]
        }
	},
	{
        "nombre": "obtener_datos_carga",
        "system_instruction": (
            "eres un asistente de inteligencia artificial que ayuda a los transportistas a extraer información de la carga y del vehículo a partir de una guía de transporte. Tu tarea es leer el texto proporcionado "
            "por el conductor y extraer la patente del vehículo, el tipo de carga, el peso, la cantidad de bultos, la ciudad de origen, la ciudad de destino y cualquier otra información importante de la carga. Devuelve los datos en formato JSON dentro de items con las claves "
            "'atributo' ,'valor' y 'calidad' (del 1 al 5 , indica la calidad del dato entregado) , y guardar la fecha de ejecucion de la peticion dentro de dateInput."
        ),
        "ejemplo_usuario": "llevo 40 cajas de fruta fresca con un peso total de 1200 kilos en el camion patente BXKL45, salgo de rancagua y voy a santiago",
        "claves_esperadas": ["dateInput", "items"],
        "response_schema": {
            "type": "object",
            "properties": {
                "dateInput": {"type": "string"},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "atributo": {"type": "string"},
                            "valor": {"type": "string"},
                            "calidad": {"type": "number"}
                        },
                        "required": ["atributo", "valor", "calidad"]
                    }
                }
            },
            "required": ["dateInput", "items"]
        }
    },
    {
        "nombre": "clasificar_incidencia",
        "system_instruction": (
            "eres un asistente de inteligencia artificial que ayuda a los transportistas a reportar incidencias ocurridas durante un viaje. Tu tarea es leer el texto proporcionado "
            "por el conductor y clasificar la incidencia. Devuelve los datos en formato JSON con las claves 'categoria' (una de: retraso, dano_carga, accidente, robo, falla_mecanica, otro), "
            "'severidad' (del 1 al 5, siendo 5 la más grave), 'resumen' (una frase corta con lo ocurrido) y 'requiere_accion_inmediata' (true o false), "
            "y guardar la fecha de ejecucion de la peticion dentro de dateInput."
        ),
        "ejemplo_usuario": "se me reventó un neumático en la ruta 5 sur a la altura de rancagua, voy a llegar dos horas tarde pero la carga esta bien",
        "claves_esperadas": ["dateInput", "categoria", "severidad", "resumen", "requiere_accion_inmediata"],
        "response_schema": {
            "type": "object",
            "properties": {
                "dateInput": {"type": "string"},
                "categoria": {
                    "type": "string",
                    "enum": ["retraso", "dano_carga", "accidente", "robo", "falla_mecanica", "otro"]
                },
                "severidad": {"type": "number"},
                "resumen": {"type": "string"},
                "requiere_accion_inmediata": {"type": "boolean"}
            },
            "required": ["dateInput", "categoria", "severidad", "resumen", "requiere_accion_inmediata"]
        }
    },
]