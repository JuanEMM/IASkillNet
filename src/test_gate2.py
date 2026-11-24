import logging

from langchain_protocol import TypedDict
 
# Dato sensible de prueba que NUNCA debe aparecer en los logs
CORREO = "ana.perez@example.com"
PREGUNTA = "Cual es la politica de devoluciones? Mi correo es " + CORREO
 
# ===== ADAPTA ESTA SECCION A TU PROYECTO =====
logger = logging.getLogger("servicio")
 
def ejecutar_servicio(pregunta):
	"""Corre tu flujo completo (indexar, recuperar y responder).
	Debe devolver (respuesta, fuentes): el texto final y la lista de fuentes usadas."""
	# Demo: reemplaza este cuerpo por la llamada a tu propio servicio.
	fuentes = ["politica_devoluciones.md"]
	logger.info("consulta recibida", extra={"pregunta_len": len(pregunta)})
	respuesta = "Puedes devolver un producto en 30 dias [fuente: politica_devoluciones.md]."
	return respuesta, fuentes
 
def crear_supervision():
    """Devuelve (app, entrada): tu grafo de supervision humana ya compilado con
    checkpointer (Bloque 32) y el estado inicial con el que se invoca."""
    # Demo: reemplaza este cuerpo por tu propio grafo.
    from typing import TypedDict
    from langgraph.graph import StateGraph, START, END
    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.types import interrupt
 
    class Estado(TypedDict):
        huella_nueva: str
        aprobado: bool
 
    def supervisar(estado: Estado):
        return {"aprobado": interrupt({"motivo": "aprobar despliegue"})}
 
    grafo = StateGraph(Estado)
    grafo.add_node("supervisar", supervisar)
    grafo.add_edge(START, "supervisar")
    grafo.add_edge("supervisar", END)
    app = grafo.compile(checkpointer=InMemorySaver())
    return app, {"huella_nueva": "abc123", "aprobado": False}
# ===== FIN DE LA SECCION A ADAPTAR =====
 
 
def test_1_pipeline_sin_excepciones():
	respuesta, _ = ejecutar_servicio(PREGUNTA)
	assert respuesta.strip(), "el servicio devolvio una respuesta vacia"
 
 
def test_2_respuesta_cita_fuente():
	respuesta, fuentes = ejecutar_servicio(PREGUNTA)
	assert fuentes, "el servicio no devolvio ninguna fuente"
	assert any(f in respuesta for f in fuentes), "la respuesta no menciona su fuente"
 
 
def test_3_logs_sin_contenido_crudo(caplog):
    with caplog.at_level(logging.DEBUG):
        ejecutar_servicio(PREGUNTA)
    texto_logs = " ".join(r.getMessage() + " " + str(r.__dict__) for r in caplog.records)
    assert CORREO not in texto_logs, "un dato sensible aparece en los logs"
    assert PREGUNTA not in texto_logs, "la consulta completa aparece en los logs"
 
 
def test_4_supervision_pausa_y_reanuda():
	from langgraph.types import Command
	app, entrada = crear_supervision()
	config = {"configurable": {"thread_id": "test-gate2"}}
	pausado = app.invoke(entrada, config=config)
	assert "__interrupt__" in pausado, "el grafo no se detuvo en el punto de supervision"
	final = app.invoke(Command(resume=True), config=config)
	assert "__interrupt__" not in final, "el grafo sigue pausado despues de reanudar"
	assert final["aprobado"] is True, "la decision no quedo registrada"