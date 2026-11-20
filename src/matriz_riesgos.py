def puntaje_riesgo(probabilidad, impacto):
	return probabilidad * impacto
 
def categoria_riesgo(puntaje):
    if puntaje >= 15:
        return "CRITICO"
    if puntaje >= 9:
        return "ALTO"
    if puntaje >= 4:
        return "MEDIO"
    return "BAJO"
mis_riesgos = [
	# Fila modelo: quita los # para ver el resultado y luego reemplaza la fila por un riesgo de tu proyecto.
	# {"riesgo": "Inyeccion de prompt via comentario de usuario indexado",
	#  "probabilidad": 4,   # 1 a 5: probable, con la informacion que tienes hoy
	#  "impacto": 4,    	# 1 a 5: expone instrucciones internas y datos de clientes
	#  "mitigacion": "Filtro de patrones + delimitacion de contexto (Bloque 31)"},
	# Tus otras filas aqui, con la misma estructura (cinco como minimo)
	{"riesgo": "Extraccion incorrecta de patente, RUT o numero de guia que registra el ingreso del camion equivocado",
	 "probabilidad": 4,   # el modelo extrae de texto libre y hoy nada valida los valores (consumir_gemini.py solo revisa que existan las claves)
	 "impacto": 4,    	# un ingreso mal asociado falsea quien esta en planta y el tiempo de permanencia
	 "mitigacion": "Validar formato de patente y digito verificador del RUT con codigo; si 'calidad' es menor a 4, el guardia confirma a mano"},
	{"riesgo": "Inyeccion de prompt via el texto que escribe o dicta el conductor",
	 "probabilidad": 3,   # el texto del conductor entra directo como 'input' (consumir_gemini.py), sin filtro ni delimitadores
	 "impacto": 4,    	# un texto hostil podria falsear datos de la guia o pedir que se ignoren las instrucciones
	 "mitigacion": "Delimitar el texto del conductor, filtrar patrones tipicos de inyeccion y dejar que el modelo solo extraiga: la autorizacion de ingreso la decide una persona"},
	{"riesgo": "Nombres de atributo inconsistentes en 'items' (rut, RUT, rut_chofer) que rompen el cruce automatico con la base de datos",
	 "probabilidad": 4,   # 'atributo' es texto libre en el schema; el 3/3 de registro_resultados.json solo mide estructura, no nombres
	 "impacto": 3,    	# el dato se extrae bien pero no se puede usar sin intervencion manual
	 "mitigacion": "Restringir 'atributo' con un enum en el schema; si las fallas siguen en 3 de 20 o mas, evaluar PEFT (docs/decision_personalizacion.md)"},
	{"riesgo": "Datos personales (RUT, nombre del chofer) enviados a la API externa y guardados en trazas y logs",
	 "probabilidad": 3,   # el RUT viaja en cada peticion y las trazas del agente se guardan en archivos .jsonl del repositorio
	 "impacto": 4,    	# filtracion de datos personales de choferes
	 "mitigacion": "Enmascarar el RUT en logs y trazas, no versionar los .jsonl con datos reales y revisar la politica de datos del proveedor"},
	{"riesgo": "Caida, limite de cuota o lentitud de la API que deja la porteria sin poder registrar ingresos",
	 "probabilidad": 4,   # enviar_peticion usa timeout=10 s y en docs/decision-arquitectura.md Gemini tardo unos 20 s por respuesta
	 "impacto": 3,    	# camiones esperando en la entrada; el control no puede depender del modelo
	 "mitigacion": "Ingreso manual de contingencia, reintentos con backoff y un timeout acorde a la latencia medida"},
	{"riesgo": "Registros de ingreso y salida incompletos (camion sin hora de salida) que falsean el tiempo en planta",
	 "probabilidad": 3,   # depende de que cada salida se registre, y hoy no hay un control que detecte pendientes
	 "impacto": 3,    	# la lista de camiones en planta y los tiempos de permanencia dejan de ser confiables
	 "mitigacion": "Alerta para camiones sin salida tras N horas y cierre de jornada que revise los pendientes"},
	{"riesgo": "Cambio o retiro del modelo (MODEL = gemini-3.5-flash-lite) que altera el formato de las respuestas",
	 "probabilidad": 3,   # decision-arquitectura.md ya menciona problemas con la actualizacion de version del modelo
	 "impacto": 2,    	# se detecta rapido con las pruebas de consistencia y se corrige ajustando el prompt
	 "mitigacion": "Fijar la version del modelo y correr prompts/test_consistencia.py antes de cada cambio"},
]
 
for r in mis_riesgos:
	r["puntaje"] = puntaje_riesgo(r["probabilidad"], r["impacto"])
	r["categoria"] = categoria_riesgo(r["puntaje"])
 
for r in sorted(mis_riesgos, key=lambda x: -x["puntaje"]):
	print(f"{r['categoria']:8} ({r['puntaje']:2}) - {r['riesgo']}")
 
 
def esta_en_el_limite(probabilidad, impacto):
    categoria_actual = categoria_riesgo(puntaje_riesgo(probabilidad, impacto))
    vecinos = [
        (probabilidad + 1, impacto), (probabilidad - 1, impacto),
        (probabilidad, impacto + 1), (probabilidad, impacto - 1),
    ]
    for p2, i2 in vecinos:
        if not (1 <= p2 <= 5 and 1 <= i2 <= 5):
            continue
        if categoria_riesgo(puntaje_riesgo(p2, i2)) != categoria_actual:
            return True
    return False

for r in mis_riesgos:
    r["al_limite"] = esta_en_el_limite(r["probabilidad"], r["impacto"])
    if r["al_limite"]:
        print("revisar con otra persona:", r["riesgo"])
  
# riesgo de contraste, deliberadamente lejos de cualquier limite
print()
print("riesgo de contraste (probabilidad=1, impacto=1):",
  	"AL LIMITE" if esta_en_el_limite(1, 1) else "no al limite",
  	"- puntaje", puntaje_riesgo(1, 1), categoria_riesgo(puntaje_riesgo(1, 1)))