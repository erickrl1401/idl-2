"""Manejo de sesión local: almacena el JWT token y datos del usuario."""

_session: dict = {}


def set_session(token: str, usuario: dict) -> None:
    """Guarda el token JWT y los datos del usuario en la sesión local."""
    _session["token"] = token
    _session["usuario"] = usuario


def get_token() -> str | None:
    """Retorna el token JWT de la sesión activa, o None si no hay sesión."""
    return _session.get("token")


def get_usuario() -> dict | None:
    """Retorna los datos del usuario de la sesión activa."""
    return _session.get("usuario")


def clear_session() -> None:
    """Cierra la sesión eliminando token y datos de usuario."""
    _session.clear()


def is_authenticated() -> bool:
    """Verifica si existe una sesión activa con token."""
    return bool(_session.get("token"))
