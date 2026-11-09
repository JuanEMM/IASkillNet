from collections import Counter
import json
from test_pipeline_texto import procesar_texto
from cliente import consultar_modelo

def contar_coincidencias(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> int: 
    conteo_referencia = Counter(tokens_referencia)
    conteo_respuesta = Counter(tokens_respuesta)
    interseccion = conteo_referencia & conteo_respuesta
    return sum(interseccion.values())

def calcular_precision_cobertura_f1(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> dict[str, float]: 
    coincidencias = contar_coincidencias(
        tokens_referencia, tokens_respuesta
    )

    if not tokens_respuesta or not tokens_referencia:
        return {"precision": 0.0, "cobertura": 0.0, "f1": 0.0}

    precision = coincidencias / len(tokens_respuesta)
    cobertura = coincidencias / len(tokens_referencia)

    if precision + cobertura == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * cobertura / (precision + cobertura)

    resultado = {
        "precision": precision,
        "cobertura": cobertura,
        "f1": f1,
    }

    return resultado
def calcular_metricas(texto_referencia, texto_respuesta):

    tokens_referencia = procesar_texto(texto_referencia)

    tokens_respuesta = procesar_texto(texto_respuesta)

    return calcular_precision_cobertura_f1(
        tokens_referencia, tokens_respuesta
    )

casos = [

    # Certeras: tienen una respuesta clara y correcta
    (
        "¿Qué es el peso bruto vehicular?",
        "Es el peso total del camión con su carga, es decir, la suma "
        "de la tara y la carga transportada.",
    ),

    (
        "¿Para qué sirve el tacógrafo?",
        "Registra la velocidad, el tiempo de conducción y los "
        "descansos del chofer.",
    ),

    (
        "¿Cuántas toneladas puede llevar un camión de 2 ejes o más?",
        "Puede llevar hasta 45 toneladas.",
    ),

    (
        "¿Qué es la tara de un camión?",
        "Es el peso del camión vacío, sin carga.",
    ),

    (
        "¿Qué es una guía de despacho?",
        "Es el documento que respalda el traslado de mercancías de "
        "un lugar a otro.",
    ),

    (
        "¿Para qué sirve una balanza de pesaje en carretera?",
        "Sirve para pesar el camión y verificar que no supere el "
        "peso máximo permitido.",
    ),

    (
        "¿Qué es una carga sobredimensionada?",
        "Es la carga que excede las dimensiones máximas permitidas "
        "de largo, ancho o alto del vehículo.",
    ),

    (
        "¿Qué es la trazabilidad de un envío?",
        "Es la posibilidad de seguir el recorrido y el estado de un "
        "envío desde su origen hasta su entrega.",
    ),

    # Ambiguas: la respuesta depende del contexto
    (
        "¿Cuál es la presión correcta de los neumáticos de un camión?",
        "Depende del fabricante, la medida del neumático y la carga "
        "que lleva el camión.",
    ),

    (
        "¿Cada cuánto se deben cambiar los neumáticos de un camión?",
        "Depende del desgaste, el uso, la carga y el tipo de ruta.",
    ),

    (
        "¿Cuánto demora un envío?",
        "Depende del origen, el destino y el medio de transporte.",
    ),

    (
        "¿Cuál es la mejor ruta de entrega?",
        "La ruta más conveniente depende del costo, el tiempo y las "
        "restricciones de cada entrega.",
    ),

    (
        "¿Cuánto combustible gasta un camión?",
        "Depende del modelo, la carga, la ruta y la forma de conducir.",
    ),

    (
        "¿Cuántas horas seguidas puede manejar un chofer?",
        "Depende de la normativa del país y del tipo de transporte.",
    ),

    (
        "¿Cuánto cuesta un flete?",
        "Depende de la distancia, el peso, el tipo de carga y el "
        "medio de transporte.",
    ),

    # Referencias falsas: cada una lleva el dato correcto en un comentario

    # Lo correcto: revisarla con frecuencia, idealmente antes de
    # cada viaje y con el neumático frío
    (
        "¿Cada cuánto se debe revisar la presión de los neumáticos?",
        "Basta revisarla una vez al año, durante la revisión técnica.",
    ),

    # Lo correcto: se mide con el neumático frío
    (
        "¿Con el neumático frío o caliente se mide la presión?",
        "Se debe medir justo después de manejar, con el neumático "
        "caliente.",
    ),

    # Lo correcto: no se puede superar el peso máximo, esté la carga
    # amarrada o no
    (
        "¿Un camión puede superar el peso máximo permitido si la "
        "carga está bien amarrada?",
        "Sí, si la carga está bien amarrada se puede superar el peso "
        "máximo.",
    ),

    # Lo correcto: nunca se le echa agua fría, hay que detenerse y
    # dejar que se enfríe solo
    (
        "¿Qué hacer si un neumático se calienta mucho en ruta?",
        "Hay que echarle agua fría de inmediato para enfriarlo.",
    ),

    # Lo correcto: el vendedor responde solo hasta cargar la
    # mercancía en el buque, no hasta el destino
    (
        "¿Qué significa FOB?",
        "FOB significa que el vendedor paga el seguro y el flete "
        "hasta el puerto de destino.",
    ),

]


resultados = []

for consulta, referencia in casos:

    respuesta = consultar_modelo(consulta)

    metricas = calcular_metricas(referencia, respuesta)

    resultados.append({
        "consulta": consulta,
        "respuesta": respuesta,
        **metricas,
    })


with open(
    "resultados_metricas.json", "w", encoding="utf-8"
) as archivo:

    json.dump(resultados, archivo, indent=2, ensure_ascii=False)



