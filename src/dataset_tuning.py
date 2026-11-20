import json
from google.genai import types
 
# Ejemplo resuelto: tickets de soporte en texto libre -> JSON con intencion y prioridad.
# Reemplaza estos casos por los de tu propio proyecto.
ejemplos_raw = [
	("No puedo iniciar sesion desde ayer: dice que mi contrasena es incorrecta aunque ya la cambie dos veces.",
 	{"intencion": "acceso", "prioridad": "alta"}),
	("Me cobraron dos veces la suscripcion de este mes, necesito el reembolso de uno de los cargos.",
 	{"intencion": "facturacion", "prioridad": "alta"}),
	("Quisiera saber si el plan Pro incluye mas de un usuario, no es urgente.",
 	{"intencion": "consulta_plan", "prioridad": "baja"}),
	("La aplicacion se cierra sola cada vez que intento subir una foto.",
 	{"intencion": "falla_tecnica", "prioridad": "media"}),
	("Quiero dar de baja mi cuenta al terminar el mes, gracias.",
 	{"intencion": "cancelacion", "prioridad": "media"}),
	("No me llega el correo para restablecer la contrasena.",
 	{"intencion": "acceso", "prioridad": "media"}),
	("Hay un cargo en mi tarjeta que no reconozco y quiero que lo revisen hoy.",
 	{"intencion": "facturacion", "prioridad": "alta"}),
]
 
examples = [
	types.TuningExample(text_input=texto, output=json.dumps(salida, ensure_ascii=False))
	for texto, salida in ejemplos_raw
]
 
print(len(examples), "ejemplos construidos")
print(examples[0])
from collections import Counter
 
 
def chequear_balance(ejemplos_raw: list[tuple[str, dict]], clave: str) -> Counter:
	categorias = Counter(salida[clave] for _, salida in ejemplos_raw)
	return categorias
 
 
# Cambia "intencion" por la clave que clasifica tus ejemplos
balance = chequear_balance(ejemplos_raw, "intencion")
for categoria, cuenta in balance.most_common():
	print(f"{categoria}: {cuenta}")
def validar_dataset(
	examples: list[types.TuningExample], claves_esperadas: tuple[str, ...]
) -> list[str]:
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
 
 
# Cambia las claves por las de tu tarea
problemas = validar_dataset(examples, claves_esperadas=("intencion", "prioridad"))
print(f"{len(examples)} ejemplos, {len(problemas)} problemas encontrados")
for p in problemas:
	print(" -", p)

import time
 
from google import genai
from google.genai import types
 
 
def esperar_a_que_termine(
	client: genai.Client, nombre_trabajo: str, intervalo_segundos: int = 30
) -> types.TuningJob:
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