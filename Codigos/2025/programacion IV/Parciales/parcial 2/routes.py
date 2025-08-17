from flask import Blueprint, jsonify
from data_loader import cargar_datos_vacunacion
from utils import simular_por_provincia

# Define el blueprint de rutas
rutas = Blueprint("rutas", __name__)

# Carga los datos una vez
datos = cargar_datos_vacunacion()

# GET /vacunas - Devuelve todos los registros
@rutas.route("/vacunas", methods=["GET"])
def obtener_todos_los_datos():
    return jsonify(datos)

# GET /vacunas/<año> - Devuelve el registro de un año específico
@rutas.route("/vacunas/<int:year>", methods=["GET"])
def obtener_por_año(año):
    resultado = next((d for d in datos if d["año"] == año), None)
    if resultado:
        return jsonify(resultado)
    return jsonify({"error": "Año no encontrado"}), 404

# GET /vacunas/provincia/<nombre> - Simula datos por provincia
@rutas.route("/vacunas/provincia/<nombre>", methods=["GET"])
def obtener_por_provincia(nombre):
    resultado = simular_por_provincia(datos, nombre)
    if resultado:
        return jsonify(resultado)
    return jsonify({"error": "Provincia no válida"}), 404
