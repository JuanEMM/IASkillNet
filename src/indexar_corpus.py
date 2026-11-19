from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()
corpus = [
    "El cliente reintenta hasta 3 veces ante un TimeoutError, con espera creciente.",
    "Los errores de autenticacion nunca se reintentan: fallan de inmediato con un "
    "ValueError.",
    "El costo de cada llamada se calcula a partir de totalTokenCount y la tarifa "
    "vigente por cada 1000 tokens.",
    "El agente de la Unidad 2.4 decide por si mismo que herramienta usar, segun la "
    "descripcion de cada una.",
    "Las pruebas unitarias del cliente usan mocks, de forma que la suite completa "
    "corre en menos de un segundo.",
]

splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)
chunks = splitter.create_documents(
    corpus, metadatas=[{"fuente": f"doc{i}.md"} for i in range(len(corpus))]
)
# Los ids doc0..docN suponen un chunk por documento (cierto con chunk_size=200).
assert len(chunks) == len(corpus), "algun documento se partio en varios chunks"
ids = [f"doc{i}" for i in range(len(chunks))]

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Rehacer el indice: se borra lo anterior para que re-ejecutar no deje duplicados.
Chroma(persist_directory="vectorstore/", embedding_function=embeddings).delete_collection()

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    ids=ids,
    persist_directory="vectorstore/",
)

vectorstore_recargado = Chroma(
    persist_directory="vectorstore/",
    embedding_function=embeddings,
)
print(vectorstore_recargado._collection.count())