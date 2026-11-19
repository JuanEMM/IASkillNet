import json
from google.genai import types
 
ejemplos_raw = [
	("TimeoutError: la conexion tardo mas de 10 segundos en responder.",
 	{"categoria": "red", "accion_sugerida": "reintentar con backoff exponencial"}),
	("ValueError: la clave de API no tiene el formato esperado.",
 	{"categoria": "autenticacion", "accion_sugerida": "revisar GEMINI_API_KEY, no reintentar"}),
	("429 RESOURCE_EXHAUSTED: se supero el limite de peticiones por minuto.",
 	{"categoria": "cuota", "accion_sugerida": "esperar y reintentar, con backoff"}),
	("API key not valid. Please pass a valid API key.",
 	{"categoria": "autenticacion", "accion_sugerida": "revisar GEMINI_API_KEY, no reintentar"}),
	("RuntimeError: Your system has an unsupported version of sqlite3.",
 	{"categoria": "entorno", "accion_sugerida": "instalar pysqlite3-binary"}),
	("ModuleNotFoundError: No module named langchain_chroma.",
 	{"categoria": "entorno", "accion_sugerida": "instalar dependencia faltante"}),
	("PermissionError al crear la carpeta del vector store.",
 	{"categoria": "entorno", "accion_sugerida": "revisar permisos de escritura"}),
	("InvalidArgumentError: Collection expecting embedding with dimension of 768, got 1536.",
 	{"categoria": "consistencia_indice", "accion_sugerida": "reindexar con el mismo modelo de embeddings"}),
]
 
examples = [
	types.TuningExample(text_input=texto, output=json.dumps(salida, ensure_ascii=False))
	for texto, salida in ejemplos_raw
]
 
print(len(examples), "ejemplos construidos")
print(examples[0])

def validar_dataset(examples, claves_esperadas=("categoria", "accion_sugerida")):
    problemas = []
    vistos = set()
    for i, ej in enumerate(examples):
        if not ej.text_input or not ej.text_input.strip():
            problemas.append(f"ejemplo {i}: text_input vacio")
        if not ej.output or not ej.output.strip():
            problemas.append(f"ejemplo {i}: output vacio")
            continue
        if ej.text_input in vistos:
            problemas.append(f"ejemplo {i}: text_input duplicado")
        vistos.add(ej.text_input)
        try:
            salida = json.loads(ej.output)
        except json.JSONDecodeError:
            problemas.append(f"ejemplo {i}: output no es JSON valido")
            continue
        for clave in claves_esperadas:
            if clave not in salida:
                problemas.append(f'ejemplo {i}: output no tiene la clave "{clave}"')
    return problemas
 
 
problemas = validar_dataset(examples)
print(f"{len(examples)} ejemplos, {len(problemas)} problemas encontrados")
for p in problemas:
	print(" -", p)

from collections import Counter
 
 
def chequear_balance(ejemplos_raw):
	categorias = Counter(salida["categoria"] for _, salida in ejemplos_raw)
	return categorias
 
 
balance = chequear_balance(ejemplos_raw)
for categoria, cuenta in balance.most_common():
	print(f"{categoria}: {cuenta}")
 
maximo = max(balance.values())
minimo = min(balance.values())
print()
print(f"categoria mas representada: {maximo} ejemplos")
print(f"categoria menos representada: {minimo} ejemplos")
print(f"razon max/min: {maximo / minimo:.1f}x")


from google.genai import types
 
print("Estados posibles de un trabajo de tuning:")
for estado in types.JobState:
	print(" ", estado)

import time
 
def esperar_a_que_termine(client, nombre_trabajo, intervalo_segundos=30):
    """Consulta el estado del trabajo hasta que termine, en cualquier sentido."""
    estados_finales = {
        types.JobState.JOB_STATE_SUCCEEDED,
        types.JobState.JOB_STATE_FAILED,
        types.JobState.JOB_STATE_CANCELLED,
        types.JobState.JOB_STATE_PARTIALLY_SUCCEEDED,
    }
    while True:
        trabajo = client.tunings.get(name=nombre_trabajo)
        print(f"estado actual: {trabajo.state}")
        if trabajo.state in estados_finales:
            return trabajo
        time.sleep(intervalo_segundos)
examples_rotos = examples + [
	types.TuningExample(text_input="", output='{"categoria": "red"}'),
	types.TuningExample(text_input=ejemplos_raw[0][0], output="no es json"),
]
problemas2 = validar_dataset(examples_rotos)
print(f"{len(examples_rotos)} ejemplos, {len(problemas2)} problemas encontrados")
for p in problemas2:
	print(" -", p)

from dotenv import load_dotenv
from google import genai
 
load_dotenv()
client = genai.Client()
 
dataset = types.TuningDataset(examples=examples)
 
config = types.CreateTuningJobConfig(
	tuning_mode=types.TuningMode.TUNING_MODE_PEFT_ADAPTER,
	adapter_size=types.AdapterSize.ADAPTER_SIZE_FOUR,
	epoch_count=5,
	tuned_model_display_name="clasificador-errores-cliente",
)
 
try:
	trabajo = client.tunings.tune(
    	base_model="models/gemini-3.6-flash",
    	training_dataset=dataset,
    	config=config,
	)
	print(trabajo)
except Exception as error:
	print("No se pudo crear el trabajo de tuning:", error)