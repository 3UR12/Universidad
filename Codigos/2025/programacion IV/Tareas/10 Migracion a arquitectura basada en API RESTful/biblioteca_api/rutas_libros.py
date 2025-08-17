from flask import Blueprint, jsonify, request
from modelos import libros

libros_bp = Blueprint("libros", __name__)

@libros_bp.route("/books", methods=["GET"])
def obtener_libros():
    return jsonify(libros), 200

@libros_bp.route("/books/<int:id>", methods=["GET"])
def obtener_libro(id):
    libro = next((l for l in libros if l["id"] == id), None)
    return (jsonify(libro), 200) if libro else (jsonify({"error": "No encontrado"}), 404)

@libros_bp.route("/books", methods=["POST"])
def agregar_libro():
    nuevo = request.get_json()
    print("Recibido:", nuevo)
    if not nuevo or "titulo" not in nuevo or "autor" not in nuevo:
        return jsonify({"error": "Datos incompletos"}), 400
    nuevo["id"] = max([l["id"] for l in libros] or [0]) + 1
    libros.append(nuevo)
    return jsonify(nuevo), 201

@libros_bp.route("/books/<int:id>", methods=["PUT"])
def actualizar_libro(id):
    datos = request.get_json()
    libro = next((l for l in libros if l["id"] == id), None)
    if not libro:
        return jsonify({"error": "No encontrado"}), 404
    libro.update(datos)
    return jsonify(libro), 200

@libros_bp.route("/books/<int:id>", methods=["DELETE"])
def eliminar_libro(id):
    global libros
    libros = [l for l in libros if l["id"] != id]
    return jsonify({"mensaje": "Eliminado"}), 200
