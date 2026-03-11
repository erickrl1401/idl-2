from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity

from api.models.usuario import UsuarioModel
from api.middleware.auth_middleware import token_required, admin_required
from api.config import Config

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    """POST /api/auth/login - Autenticar usuario y retornar JWT."""
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400

    usuario = UsuarioModel.get_by_email(email)
    if not usuario or not UsuarioModel.verify_password(password, usuario["password_hash"]):
        return jsonify({"error": "Credenciales inválidas"}), 401

    expires = timedelta(hours=Config.JWT_ACCESS_TOKEN_EXPIRES_HOURS)
    token = create_access_token(
        identity=str(usuario["id"]),
        expires_delta=expires,
        additional_claims={"rol": usuario["rol"], "nombre": usuario["nombre"]},
    )
    return jsonify({
        "token": token,
        "usuario": {
            "id": usuario["id"],
            "nombre": usuario["nombre"],
            "email": usuario["email"],
            "rol": usuario["rol"],
        },
    }), 200


@auth_bp.route("/register", methods=["POST"])
@admin_required
def register():
    """POST /api/auth/register - Registrar nuevo usuario (solo admin)."""
    data = request.get_json(silent=True) or {}
    nombre = data.get("nombre", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    rol = data.get("rol", "empleado")

    if not nombre or not email or not password:
        return jsonify({"error": "nombre, email y password son requeridos"}), 400
    if rol not in ("admin", "empleado"):
        return jsonify({"error": "Rol inválido. Use 'admin' o 'empleado'"}), 400

    if UsuarioModel.get_by_email(email):
        return jsonify({"error": "El email ya está registrado"}), 409

    nuevo_id = UsuarioModel.create(nombre, email, password, rol)
    return jsonify({"mensaje": "Usuario creado", "id": nuevo_id}), 201


@auth_bp.route("/perfil", methods=["GET"])
@token_required
def perfil():
    """GET /api/auth/perfil - Retornar datos del usuario autenticado."""
    usuario_id = int(get_jwt_identity())
    usuario = UsuarioModel.get_by_id(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({"usuario": usuario}), 200
