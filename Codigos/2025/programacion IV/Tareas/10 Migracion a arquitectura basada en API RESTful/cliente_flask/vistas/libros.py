import os
import requests
from flask import Blueprint, render_template, request, redirect, flash, url_for
from dotenv import load_dotenv

load_dotenv()
libros_bp = Blueprint("libros", __name__)
API_URL = os.getenv("API_URL", "http://127.0.0.1:5001")

@libros_bp.route("/", methods=["GET"])
def mostrar_libros():
    try:
        respuesta = requests.get(f"{API_URL}/books")
        libros = respuesta.json()
    except Exception as e:
        libros = []
        flash("Error al conectar con la API", "error")
    return render_template("libros.html", libros=libros)

@libros_bp.route("/agregar", methods=["POST"])
def agregar_libro():
    datos = {
        "titulo": request.form.get("titulo", "").strip(),
        "autor": request.form.get("autor", "").strip()
    }

    if not datos["titulo"] or not datos["autor"]:
        flash("Título y autor son obligatorios", "error")
        return redirect(url_for("libros.mostrar_libros"))

    try:
        respuesta = requests.post(f"{API_URL}/books", json=datos)
        if respuesta.status_code == 201:
            flash("Libro agregado correctamente", "exito")
        else:
            flash("Error al agregar libro", "error")
    except Exception:
        flash("No se pudo conectar con la API", "error")

    return redirect(url_for("libros.mostrar_libros"))
