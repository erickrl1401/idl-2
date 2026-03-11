from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt

from api.models.cliente import ClienteModel
from api.middleware.auth_middleware import token_required

cliente_bp = Blueprint("clientes", __name__, url_prefix="/api/clientes")


@cliente_bp.route("", methods=["GET"])
@token_required
def listar_clientes():
    """GET /api/clientes - Lista todos los clientes activos con paginación."""
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    resultado = ClienteModel.get_all(page=page, per_page=per_page)
    return jsonify(resultado), 200


@cliente_bp.route("/buscar", methods=["GET"])
@token_required
def buscar_clientes():
    """GET /api/clientes/buscar?q=... - Buscar clientes."""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Parámetro 'q' es requerido"}), 400
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    resultado = ClienteModel.search(query, page=page, per_page=per_page)
    return jsonify(resultado), 200


@cliente_bp.route("/<int:cliente_id>", methods=["GET"])
@token_required
def obtener_cliente(cliente_id):
    """GET /api/clientes/<id> - Obtener un cliente por ID."""
    cliente = ClienteModel.get_by_id(cliente_id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    return jsonify({"cliente": cliente}), 200


@cliente_bp.route("", methods=["POST"])
@token_required
def crear_cliente():
    """POST /api/clientes - Crear nuevo cliente."""
    data = request.get_json(silent=True) or {}
    if not data.get("nombre") or not data.get("apellido"):
        return jsonify({"error": "nombre y apellido son requeridos"}), 400

    usuario_id = int(get_jwt_identity())
    nuevo_id = ClienteModel.create(data, created_by=usuario_id)
    cliente = ClienteModel.get_by_id(nuevo_id)
    return jsonify({"mensaje": "Cliente creado", "cliente": cliente}), 201


@cliente_bp.route("/<int:cliente_id>", methods=["PUT"])
@token_required
def actualizar_cliente(cliente_id):
    """PUT /api/clientes/<id> - Actualizar datos de un cliente."""
    data = request.get_json(silent=True) or {}
    if not ClienteModel.get_by_id(cliente_id):
        return jsonify({"error": "Cliente no encontrado"}), 404

    ClienteModel.update(cliente_id, data)
    cliente = ClienteModel.get_by_id(cliente_id)
    return jsonify({"mensaje": "Cliente actualizado", "cliente": cliente}), 200


@cliente_bp.route("/<int:cliente_id>", methods=["DELETE"])
@token_required
def eliminar_cliente(cliente_id):
    """DELETE /api/clientes/<id> - Eliminar (desactivar) un cliente."""
    if not ClienteModel.get_by_id(cliente_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
    ClienteModel.delete(cliente_id)
    return jsonify({"mensaje": "Cliente eliminado"}), 200
