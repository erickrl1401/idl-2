from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt


def token_required(f):
    """Decorador que verifica que el request incluya un JWT válido."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"error": "Token inválido o expirado", "detalle": str(e)}), 401
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Decorador que verifica que el usuario autenticado tenga rol 'admin'."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"error": "Token inválido o expirado", "detalle": str(e)}), 401
        claims = get_jwt()
        if claims.get("rol") != "admin":
            return jsonify({"error": "Se requieren permisos de administrador"}), 403
        return f(*args, **kwargs)
    return decorated
