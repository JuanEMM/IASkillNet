import re
from collections import Counter

def limpiar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

def tokenizar(texto_limpio: str) -> list[str]:
    return texto_limpio.split()

def vectorizar(tokens: list[str]) -> Counter: 
    return Counter(tokens)

def procesar_texto(texto):
    texto_limpio = limpiar_texto(texto)
    return tokenizar(texto_limpio)
if __name__ == "__main__":
    texto = "El gato, el perro y el gato corren."

    texto_limpio = limpiar_texto(texto)

    tokens = tokenizar(texto_limpio)

    conteo = vectorizar(tokens)

    print("Texto limpio:", texto_limpio)

    print("Tokens:", tokens)

    print("Conteo:", conteo)