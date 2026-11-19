from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

PROMPT_TEMPLATE = """Responde la pregunta usando SOLO el contexto de abajo. Cita la \
fuente de cada afirmacion con su numero entre corchetes, como [1]. Si el contexto no \
alcanza para responder, dilo explicitamente en vez de inventar.

Contexto:
{contexto}

Pregunta: {pregunta}

Respuesta:"""

def formatear_contexto(chunks_recuperados):
    """Arma un bloque de contexto numerado para el prompt, y un mapa
    numero -> fuente para reconstruir la cita despues."""
    lineas = []
    citas = {}
    for i, doc in enumerate(chunks_recuperados, start=1):
        fuente = doc.metadata.get("fuente", "desconocida")
        lineas.append(f"[{i}] {doc.page_content}")
        citas[i] = fuente
    contexto = "\n\n".join(lineas)
    return contexto, citas

def construir_prompt(pregunta, persist_directory, k=3):
    """Recupera los k chunks mas relevantes para la pregunta y arma
    el prompt
    dinamico con contexto numerado, listo para pasarle al modelo."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    chunks_recuperados = retriever.invoke(pregunta)
    contexto, citas = formatear_contexto(chunks_recuperados)
    prompt = PROMPT_TEMPLATE.format(contexto=contexto, pregunta=pregunta)
    return prompt, citas

if __name__ == "__main__":
    prompt, citas = construir_prompt(
        "como decide el agente que herramienta usar",
        persist_directory="vectorstore/",
    )
    print(prompt)
    print(citas)


from langchain_core.documents import Document

chunks_ejemplo = [
    Document(
        page_content="El cliente reintenta hasta 3 veces ante un TimeoutError.",
        metadata={"fuente": "doc0.md"},
    ),
    Document(
        page_content="El costo de cada llamada se calcula a partir de totalTokenCount.",
        metadata={"fuente": "doc2.md"},
    ),
]
contexto_ejemplo, citas_ejemplo = formatear_contexto(chunks_ejemplo)
print(citas_ejemplo)