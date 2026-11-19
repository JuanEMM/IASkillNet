from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
 
load_dotenv()
 
K = 3  # cuantos chunks recupera el retriever y cuantos evalua la funcion

# Conjunto de evaluacion. Etiquetado leyendo el corpus (vectorstore/, ids doc0..doc4),
# ANTES de ver que devuelve el retriever:
#   doc0: reintenta hasta 3 veces ante TimeoutError, con espera creciente
#   doc1: errores de autenticacion nunca se reintentan, fallan con ValueError
#   doc2: el costo sale de totalTokenCount y la tarifa por cada 1000 tokens
#   doc3: el agente decide que herramienta usar segun la descripcion de cada una
#   doc4: pruebas unitarias del cliente usan mocks, suite completa en < 1 segundo
casos_evaluacion = [
    # --- doc0: reintentos ante timeout ---
    {"pregunta": "cuantas veces vuelve a intentar el cliente una llamada que excede el tiempo de espera",
     "ids_relevantes": {"doc0"}},
    {"pregunta": "como es la pausa entre un reintento y el siguiente",
     "ids_relevantes": {"doc0"}},
    # --- doc1: errores de autenticacion ---
    {"pregunta": "se reintenta una llamada cuando falla la autenticacion",
     "ids_relevantes": {"doc1"}},
    {"pregunta": "que excepcion aparece cuando las credenciales no son validas",
     "ids_relevantes": {"doc1"}},
    # --- doc2: costo por llamada ---
    {"pregunta": "de donde sale el dato que se usa para calcular cuanto cuesta cada llamada",
     "ids_relevantes": {"doc2"}},
    {"pregunta": "como se obtiene el precio de una llamada segun los tokens consumidos",
     "ids_relevantes": {"doc2"}},
    # --- doc3: agente y herramientas ---
    {"pregunta": "quien elige la herramienta que se ejecuta en cada paso",
     "ids_relevantes": {"doc3"}},
    {"pregunta": "en que se basa el agente para escoger una herramienta",
     "ids_relevantes": {"doc3"}},
    # --- doc4: pruebas unitarias ---
    {"pregunta": "por que las pruebas del cliente corren tan rapido",
     "ids_relevantes": {"doc4"}},
    {"pregunta": "que tecnica se usa en las pruebas para no depender de servicios externos",
     "ids_relevantes": {"doc4"}},
    # --- pregunta que necesita dos chunks ---
    {"pregunta": "que errores del cliente se reintentan y cuales fallan de inmediato",
     "ids_relevantes": {"doc0", "doc1"}},
    # --- pregunta fuera del corpus: no hay nada relevante que recuperar ---
    {"pregunta": "cual es la politica de devoluciones de la tienda",
     "ids_relevantes": set()},
]
 
 
 
def precision_at_k(ids_recuperados, ids_relevantes):
    """Fraccion de los ids recuperados que son relevantes (0.0 si no hay ninguno)."""
    if not ids_recuperados:
        return 0.0
    acertados = [i for i in ids_recuperados if i in ids_relevantes]
    return len(acertados) / len(ids_recuperados)
 
 
def recall_at_k(ids_recuperados, ids_relevantes):
    """Fraccion de los ids relevantes que se recuperaron (None si el caso no tiene ninguno)."""
    if not ids_relevantes:
        return None
    acertados = [i for i in ids_recuperados if i in ids_relevantes]
    return len(acertados) / len(ids_relevantes)
 
 
def promediar(valores):
	"""Promedio que ignora los None y evita dividir por cero."""
	validos = [v for v in valores if v is not None]
	return sum(validos) / len(validos) if validos else 0.0
 
 
def evaluar_recuperacion(retriever, casos, k=3):
    """Corre cada caso contra el retriever real y promedia precision y recall."""
    resultados = []
    for caso in casos:
        chunks = retriever.invoke(caso["pregunta"])
        ids_recuperados = [c.id for c in chunks][:k]
        p = precision_at_k(ids_recuperados, caso["ids_relevantes"])
        r = recall_at_k(ids_recuperados, caso["ids_relevantes"])
        resultados.append({"pregunta": caso["pregunta"], "precision": p, "recall": r})
 
    precision_promedio = promediar(x["precision"] for x in resultados)
    recall_promedio = promediar(x["recall"] for x in resultados)
    return resultados, precision_promedio, recall_promedio

 
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = Chroma(persist_directory="vectorstore/", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": K})
 
resultados, precision_promedio, recall_promedio = evaluar_recuperacion(
	retriever, casos_evaluacion, k=K
)
 
for r in resultados:
	recall_txt = "n/a" if r["recall"] is None else f"{r['recall']:.2f}"
	print(f"{r['precision']:.2f}  {recall_txt}  {r['pregunta']}")
print(f"\npromedio -> precision: {precision_promedio:.3f}  recall: {recall_promedio:.3f}")

from datetime import date
 
with open("docs\\resultados_evaluacion.txt", "w", encoding="utf-8") as archivo:
    archivo.write(f"Fecha: {date.today()}\n")
    archivo.write(f"Configuracion: k={K}, chunk_size=200, chunk_overlap=30\n\n")
    for r in resultados:
        recall_txt = "n/a" if r["recall"] is None else f"{r['recall']:.2f}"
        archivo.write(f"{r['precision']:.2f}  {recall_txt}  {r['pregunta']}\n")
    archivo.write(
        f"\npromedio -> precision: {precision_promedio:.3f}  recall: {recall_promedio:.3f}\n"
    )
print("Resultados guardados en resultados_evaluacion.txt")