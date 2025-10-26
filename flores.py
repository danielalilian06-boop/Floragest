# flores.py
from flask import Blueprint, request, jsonify

flores_bp = Blueprint('flores', __name__)

# Base de datos simulada
DB_FLORES = [
    {"id": 1, "nombre": "Rosa", "color": "Rojo", "stock": 20, "precio": 15.5},
    {"id": 2, "nombre": "Tulipán", "color": "Amarillo", "stock": 12, "precio": 12.0}
]
NEXT_FLOR_ID = 3

# --- VALIDACIONES ---
def validar_flor(data):
    if not data.get("nombre") or not data.get("color"):
        return "El nombre y color son obligatorios."
    if not isinstance(data.get("stock"), int) or data["stock"] < 0:
        return "El stock debe ser un número entero positivo."
    if not isinstance(data.get("precio"), (int, float)) or data["precio"] <= 0:
        return "El precio debe ser un número positivo."
    return None

# --- CRUD ---
@flores_bp.route('/api/flores', methods=['GET'])
def obtener_flores():
    return jsonify(DB_FLORES)

@flores_bp.route('/api/flores', methods=['POST'])
def agregar_flor():
    global NEXT_FLOR_ID
    data = request.get_json()
    error = validar_flor(data)
    if error:
        return jsonify({"mensaje": error}), 400

    nueva_flor = {
        "id": NEXT_FLOR_ID,
        "nombre": data["nombre"],
        "color": data["color"],
        "stock": data["stock"],
        "precio": data["precio"]
    }
    DB_FLORES.append(nueva_flor)
    NEXT_FLOR_ID += 1
    return jsonify({"mensaje": "Flor agregada correctamente"}), 201

@flores_bp.route('/api/flores/<int:flor_id>', methods=['PUT'])
def actualizar_flor(flor_id):
    data = request.get_json()
    error = validar_flor(data)
    if error:
        return jsonify({"mensaje": error}), 400

    for flor in DB_FLORES:
        if flor["id"] == flor_id:
            flor.update(data)
            return jsonify({"mensaje": "Flor actualizada"}), 200
    return jsonify({"mensaje": "Flor no encontrada"}), 404

@flores_bp.route('/api/flores/<int:flor_id>', methods=['DELETE'])
def eliminar_flor(flor_id):
    global DB_FLORES
    DB_FLORES = [f for f in DB_FLORES if f["id"] != flor_id]
    return jsonify({"mensaje": "Flor eliminada"}), 200
