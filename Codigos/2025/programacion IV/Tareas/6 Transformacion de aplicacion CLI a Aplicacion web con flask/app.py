from flask import Flask, render_template, request, redirect, url_for, flash
from config import ConfiguracionAplicacion
from conexion_keydb import obtener_conexion_keydb
from gestor_libros import (
    guardar_libro,
    obtener_libro_por_id,
    actualizar_libro,
    eliminar_libro,
    obtener_todos_los_libros,
    buscar_libros_por_campo
)

# Inicializa la aplicación Flask
app = Flask(__name__)
app.config.from_object(ConfiguracionAplicacion)

# Conexión con KeyDB
conexion = obtener_conexion_keydb()

@app.route("/")
def mostrar_libros():
    """
    Muestra todos los libros registrados.
    """
    libros = obtener_todos_los_libros(conexion)
    return render_template("listado_libros.html", libros=libros)

@app.route("/agregar", methods=["GET", "POST"])
def agregar_libro():
    """
    Muestra el formulario para agregar un libro y guarda los datos.
    """
    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        genero = request.form["genero"]
        estado = request.form["estado"]
        guardar_libro(conexion, titulo, autor, genero, estado)
        flash("Libro agregado correctamente.")
        return redirect(url_for("mostrar_libros"))
    return render_template("formulario_libro.html", libro=None)

@app.route("/editar/<id_libro>", methods=["GET", "POST"])
def editar_libro(id_libro):
    """
    Muestra el formulario para editar un libro y actualiza los datos.
    """
    libro = obtener_libro_por_id(conexion, id_libro)
    if not libro:
        flash("Libro no encontrado.")
        return redirect(url_for("mostrar_libros"))

    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        genero = request.form["genero"]
        estado = request.form["estado"]
        actualizar_libro(conexion, id_libro, titulo, autor, genero, estado)
        flash("Libro actualizado correctamente.")
        return redirect(url_for("mostrar_libros"))

    return render_template("formulario_libro.html", libro=libro)

@app.route("/eliminar/<id_libro>")
def eliminar_libro_por_id(id_libro):
    """
    Elimina un libro por su ID.
    """
    eliminar_libro(conexion, id_libro)
    flash("Libro eliminado correctamente.")
    return redirect(url_for("mostrar_libros"))

@app.route("/buscar", methods=["GET", "POST"])
def buscar_libros():
    """
    Muestra el formulario de búsqueda y los resultados.
    """
    resultados = []
    if request.method == "POST":
        campo = request.form["campo"]
        valor = request.form["valor"]
        resultados = buscar_libros_por_campo(conexion, campo, valor)
    return render_template("buscar_libros.html", resultados=resultados)

if __name__ == "__main__":
    app.run(debug=True)
