"""Cliente HTTP que consume la API REST del backend Flask."""

import os
import requests
from desktop.utils.session import get_token

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000/api")
TIMEOUT = 10


def _headers() -> dict:
    token = get_token()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


# ---------------------------------------------------------------------------
# Autenticación
# ---------------------------------------------------------------------------

def login(email: str, password: str) -> dict:
    resp = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def get_perfil() -> dict:
    resp = requests.get(f"{BASE_URL}/auth/perfil", headers=_headers(), timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def register(nombre: str, email: str, password: str, rol: str = "empleado") -> dict:
    resp = requests.post(
        f"{BASE_URL}/auth/register",
        json={"nombre": nombre, "email": email, "password": password, "rol": rol},
        headers=_headers(),
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Clientes
# ---------------------------------------------------------------------------

def get_clientes(page: int = 1, per_page: int = 10) -> dict:
    resp = requests.get(
        f"{BASE_URL}/clientes",
        params={"page": page, "per_page": per_page},
        headers=_headers(),
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def buscar_clientes(query: str, page: int = 1, per_page: int = 10) -> dict:
    resp = requests.get(
        f"{BASE_URL}/clientes/buscar",
        params={"q": query, "page": page, "per_page": per_page},
        headers=_headers(),
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def get_cliente(cliente_id: int) -> dict:
    resp = requests.get(f"{BASE_URL}/clientes/{cliente_id}", headers=_headers(), timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def crear_cliente(data: dict) -> dict:
    resp = requests.post(f"{BASE_URL}/clientes", json=data, headers=_headers(), timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def actualizar_cliente(cliente_id: int, data: dict) -> dict:
    resp = requests.put(
        f"{BASE_URL}/clientes/{cliente_id}",
        json=data,
        headers=_headers(),
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def eliminar_cliente(cliente_id: int) -> dict:
    resp = requests.delete(
        f"{BASE_URL}/clientes/{cliente_id}",
        headers=_headers(),
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()
