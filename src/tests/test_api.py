"""Ejecuta la tabla de casos desde dentro, sin servidor (Bloque 36).

Uso, desde la raiz del repositorio (pytest.ini agrega src/ a la ruta de importacion):
    python -m pytest -q
Los casos marcados con "modelo": True llaman a Gemini; sin GEMINI_API_KEY se omiten.
"""
import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from casos import CASOS, ejecutar_caso
from servicio.main import app

load_dotenv()
cliente = TestClient(app, raise_server_exceptions=False)
HAY_CLAVE = bool(os.getenv("GEMINI_API_KEY"))


@pytest.mark.parametrize("caso", CASOS, ids=[c["id"] for c in CASOS])
def test_caso(caso):
    if caso.get("modelo") and not HAY_CLAVE:
        pytest.skip("necesita GEMINI_API_KEY en .env")
    ok, estado, cuerpo = ejecutar_caso(cliente, caso)
    assert ok, (
        f"{caso['id']}: esperado {caso['estado']} con "
        f"{caso['contiene']!r}, obtenido {estado}: {cuerpo[:80]}"
    )
