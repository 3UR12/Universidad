from flask import Flask, request, redirect, url_for, flash
from tareas.correo import enviar_correo
import os

app = Flask(__name__)
app.secret_key = "clave_segura"

@app.route("/agregar", methods=["POST"])
def agregar_libro():
    titulo = request.form["titulo"]
    autor = request.form["autor"]
    # lógica para guardar libro...
    flash("Libro agregado exitosamente.")
    
    cuerpo = f"Se ha agregado el libro: {titulo} de {autor}."
    enviar_correo.delay(os.getenv("MAIL_USERNAME"), "Nuevo libro agregado", cuerpo)
    
    return redirect(url_for("mostrar_libros"))
