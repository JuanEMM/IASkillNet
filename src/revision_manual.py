revision_manual = [
  {
    "consulta": "¿Qué es el peso bruto vehicular?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"peso bruto vehicular\",\n      \"valor\": \"Es el peso máximo autorizado de un vehículo, que incluye su propia masa más la carga útil, los pasajeros y el combustible.\",\n      \"calidad\": 1.0\n    }\n  ]\n}",
    "precision": 0.25,
    "cobertura": 0.4,
    "f1": 0.3076923076923077
  },
  {
    "consulta": "¿Para qué sirve el tacógrafo?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"funcion_principal\",\n      \"valor\": \"Registrar la velocidad y la actividad del conductor\",\n      \"calidad\": 5\n    },\n    {\n      \"atributo\": \"control_legal\",\n      \"valor\": \"Garantizar el cumplimiento de los tiempos de conducción y descanso\",\n      \"calidad\": 5\n    },\n    {\n      \"atributo\": \"seguridad_vial\",\n      \"valor\": \"Prevenir la fatiga al volante en el transporte profesional\",\n      \"calidad\": 5\n    }\n  ]\n}",
    "precision": 0.17777777777777778,
    "cobertura": 0.6666666666666666,
    "f1": 0.2807017543859649
  },
  {
    "consulta": "¿Cuántas toneladas puede llevar un camión de 2 ejes o más?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"peso_maximo_2_ejes\",\n      \"valor\": \"15 toneladas\",\n      \"calidad\": 0.95\n    },\n    {\n      \"atributo\": \"peso_maximo_3_ejes\",\n      \"valor\": \"23 a 26 toneladas\",\n      \"calidad\": 0.95\n    },\n    {\n      \"atributo\": \"peso_maximo_4_ejes_o_mas\",\n      \"valor\": \"Hasta 31 toneladas o mas dependiendo de la configuracion\",\n      \"calidad\": 0.90\n    }\n  ]\n}",
    "precision": 0.06060606060606061,
    "cobertura": 0.4,
    "f1": 0.10526315789473685
  },
  {
    "consulta": "¿Qué es la tara de un camión?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-27\",\n  \"items\": [\n    {\n      \"atributo\": \"Definición\",\n      \"valor\": \"La tara de un camión es el peso del vehículo vacío, sin carga ni pasajeros, pero con su equipamiento fijo, depósito de combustible lleno y líquidos necesarios para su funcionamiento.\",\n      \"calidad\": 1.0\n    },\n    {\n      \"atributo\": \"Importancia\",\n      \"valor\": \"Es fundamental para calcular la carga útil que el camión puede transportar legalmente sin superar el Peso Máximo Autorizado (PMA).\",\n      \"calidad\": 1.0\n    }\n  ]\n}",
    "precision": 0.12698412698412698,
    "cobertura": 1.0,
    "f1": 0.22535211267605632
  },
  {
    "consulta": "¿Qué es una guía de despacho?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"Definicion\",\n      \"valor\": \"Documento mercantil que respalda el traslado de mercaderias.\",\n      \"calidad\": 5\n    },\n    {\n      \"atributo\": \"Uso principal\",\n      \"valor\": \"Control de inventario y verificacion de entrega entre comprador y vendedor.\",\n      \"calidad\": 5\n    }\n  ]\n}",
    "precision": 0.21212121212121213,
    "cobertura": 0.5,
    "f1": 0.2978723404255319
  },
  {
    "consulta": "¿Para qué sirve una balanza de pesaje en carretera?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"Control de peso\",\n      \"valor\": \"Verificar que los vehículos de carga no superen los límites de peso permitidos por la ley.\",\n      \"calidad\": 5.0\n    },\n    {\n      \"atributo\": \"Seguridad vial\",\n      \"valor\": \"Prevenir accidentes causados por la sobrecarga que afecta la frenada y estabilidad.\",\n      \"calidad\": 5.0\n    },\n    {\n      \"atributo\": \"Protección de infraestructura\",\n      \"valor\": \"Evitar el deterioro prematuro y daño estructural en pavimentos, puentes y carreteras.\",\n      \"calidad\": 5.0\n    },\n    {\n      \"atributo\": \"Competencia justa\",\n      \"valor\": \"Garantizar que todas las empresas de transporte operen bajo las mismas reglas y costos.\",\n      \"calidad\": 4.5\n    }\n  ]\n}",
    "precision": 0.07228915662650602,
    "cobertura": 0.42857142857142855,
    "f1": 0.12371134020618557
  },
  {
    "consulta": "¿Qué es una carga sobredimensionada?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"definicion\",\n      \"valor\": \"Una carga sobredimensionada es aquella que excede las dimensiones estandar de peso, alto, ancho o largo permitidas por la ley para la circulacion en carreteras y vias publicas.\",\n      \"calidad\": 1.0\n    },\n    {\n      \"atributo\": \"ejemplo\",\n      \"valor\": \"Equipamiento industrial pesado, aspas de aerogeneradores, modulos prefabricados y maquinaria de construccion.\",\n      \"calidad\": 0.95\n    },\n    {\n      \"atributo\": \"requisito\",\n      \"valor\": \"Requiere permisos especiales de transporte, rutas planificadas, escoltas o vehiculos piloto y senalizacion especifica.\",\n      \"calidad\": 0.98\n    }\n  ]\n}",
    "precision": 0.18055555555555555,
    "cobertura": 0.8125,
    "f1": 0.29545454545454547
  },
  {
    "consulta": "¿Qué es la trazabilidad de un envío?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-24\",\n  \"items\": [\n    {\n      \"atributo\": \"concepto\",\n      \"valor\": \"La trazabilidad de un envío es el proceso de seguimiento que permite conocer la ubicación y el estado de un paquete en tiempo real desde su origen hasta su destino final.\",\n      \"calidad\": 1.0\n    }\n  ]\n}",
    "precision": 0.38461538461538464,
    "cobertura": 0.7894736842105263,
    "f1": 0.5172413793103449
  },
  {
    "consulta": "¿Cuál es la presión correcta de los neumáticos de un camión?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"Presión de neumáticos de camión\",\n      \"valor\": \"Entre 85 y 105 PSI\",\n      \"calidad\": 95.5\n    }\n  ]\n}",
    "precision": 0.11764705882352941,
    "cobertura": 0.14285714285714285,
    "f1": 0.12903225806451615
  },
  {
    "consulta": "¿Cada cuánto se deben cambiar los neumáticos de un camión?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"Kilometraje promedio\",\n      \"valor\": \"Entre 50.000 y 100.000 kilómetros\",\n      \"calidad\": 90.0\n    },\n    {\n      \"atributo\": \"Tiempo máximo recomendado\",\n      \"valor\": \"5 a 10 años\",\n      \"calidad\": 85.0\n    },\n    {\n      \"atributo\": \"Profundidad mínima del dibujo (legal)\",\n      \"valor\": \"1.6 milímetros\",\n      \"calidad\": 95.0\n    }\n  ]\n}",
    "precision": 0.05555555555555555,
    "cobertura": 0.16666666666666666,
    "f1": 0.08333333333333333
  },
  {
    "consulta": "¿Cuánto demora un envío?",
    "respuesta": "{\"dateInput\": \"2023-10-25\", \"items\": [{\"atributo\": \"tiempo de demora\", \"valor\": \"3 a 5 días hábiles\", \"calidad\": 5}]}",
    "precision": 0.06666666666666667,
    "cobertura": 0.1,
    "f1": 0.08
  },
  {
    "consulta": "¿Cuál es la mejor ruta de entrega?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"ruta_principal\",\n      \"valor\": \"Avenida Central\",\n      \"calidad\": 9.5\n    }\n  ]\n}",
    "precision": 0.0,
    "cobertura": 0.0,
    "f1": 0.0
  },
  {
    "consulta": "¿Cuánto combustible gasta un camión?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"consumo_promedio\",\n      \"valor\": \"30 a 40 litros cada 100 kilómetros\",\n      \"calidad\": 0.85\n    }\n  ]\n}",
    "precision": 0.0,
    "cobertura": 0.0,
    "f1": 0.0
  },
  {
    "consulta": "¿Cuántas horas seguidas puede manejar un chofer?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"horas seguidas de manejo\",\n      \"valor\": \"5 horas\",\n      \"calidad\": 0.95\n    }\n  ]\n}",
    "precision": 0.07692307692307693,
    "cobertura": 0.09090909090909091,
    "f1": 0.08333333333333334
  },
  {
    "consulta": "¿Cuánto cuesta un flete?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"costo_flete\",\n      \"valor\": \"variable\",\n      \"calidad\": 0.0\n    }\n  ]\n}",
    "precision": 0.0,
    "cobertura": 0.0,
    "f1": 0.0
  },
  {
    "consulta": "¿Cada cuánto se debe revisar la presión de los neumáticos?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"frecuencia_revision_neumaticos\",\n      \"valor\": \"Una vez al mes\",\n      \"calidad\": 0.95\n    }\n  ]\n}",
    "precision": 0.25,
    "cobertura": 0.3,
    "f1": 0.2727272727272727
  },
  {
    "consulta": "¿Con el neumático frío o caliente se mide la presión?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-27\",\n  \"items\": [\n    {\n      \"atributo\": \"condicion_neumatico\",\n      \"valor\": \"frio\",\n      \"calidad\": 1.0\n    }\n  ]\n}",
    "precision": 0.0,
    "cobertura": 0.0,
    "f1": 0.0
  },
  {
    "consulta": "¿Un camión puede superar el peso máximo permitido si la carga está bien amarrada?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"peso_maximo_permitido\",\n      \"valor\": \"no\",\n      \"calidad\": 1.0\n    },\n    {\n      \"atributo\": \"seguridad_carga\",\n      \"valor\": \"irrelevante_para_el_limite_de_peso\",\n      \"calidad\": 1.0\n    }\n  ]\n}",
    "precision": 0.0,
    "cobertura": 0.0,
    "f1": 0.0
  },
  {
    "consulta": "¿Qué hacer si un neumático se calienta mucho en ruta?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"Paso 1\",\n      \"valor\": \"Detenerse inmediatamente en un lugar seguro y apartado del tráfico.\",\n      \"calidad\": 10\n    },\n    {\n      \"atributo\": \"Paso 2\",\n      \"valor\": \"Evitar arrojar agua fría sobre el neumático caliente para prevenir deformaciones o daños estructurales por el choque térmico.\",\n      \"calidad\": 9\n    },\n    {\n      \"atributo\": \"Paso 3\",\n      \"valor\": \"Dejar que el vehículo y el neumático se enfríen de manera natural durante al menos 30 a 45 minutos.\",\n      \"calidad\": 10\n    },\n    {\n      \"atributo\": \"Paso 4\",\n      \"valor\": \"Revisar la presión del neumático una vez frío y verificar si hay signos de daños, objetos punzantes o desgaste irregular.\",\n      \"calidad\": 9\n    }\n  ]\n}",
    "precision": 0.06382978723404255,
    "cobertura": 0.6666666666666666,
    "f1": 0.11650485436893203
  },
  {
    "consulta": "¿Qué significa FOB?",
    "respuesta": "{\n  \"dateInput\": \"2023-10-25\",\n  \"items\": [\n    {\n      \"atributo\": \"Significado\",\n      \"valor\": \"Free On Board (Libre a bordo)\",\n      \"calidad\": 1.0\n    },\n    {\n      \"atributo\": \"Definicion\",\n      \"valor\": \"Incoterm que indica que el vendedor entrega la mercancia a bordo del buque designado por el comprador.\",\n      \"calidad\": 1.0\n    }\n  ]\n}",
    "precision": 0.1111111111111111,
    "cobertura": 0.25,
    "f1": 0.15384615384615383
  }
]



import json



with open(

    "revision_manual.json", "w", encoding="utf-8"

) as archivo:

    json.dump(

        revision_manual, archivo, indent=2, ensure_ascii=False

    )