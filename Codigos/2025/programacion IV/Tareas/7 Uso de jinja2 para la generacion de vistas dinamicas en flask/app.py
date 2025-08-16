from flask import Flask, render_template, request, redirect, url_for, flash
from redis import Redis
import uuid
from config import REDIS_CONFIG

app = Flask(__name__)
app.secret_key = "clave_secreta"
db = Redis(**REDIS_CONFIG)

def obtener_libros():
    claves = db.keys("libro:*")
    libros = []
    for clave in claves:
        if db.type(clave) != "hash":
            continue
        libro = db.hgetall(clave)
        libro["id"] = clave.split(":")[1]
        libros.append(libro)
    return libros

@app.route("/")
def mostrar_libros():
    libros = obtener_libros()
    return render_template("listado_libros.html", libros=libros)

@app.route("/agregar", methods=["GET", "POST"])
def agregar_libro():
    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        autor = request.form["autor"].strip()
        genero = request.form["genero"].strip()
        estado = request.form["estado"]

        if not titulo or not autor or not genero:
            flash("Todos los campos son obligatorios.")
            return redirect(url_for("agregar_libro"))

        id_libro = str(uuid.uuid4())
        db.hset(f"libro:{id_libro}", mapping={
            "titulo": titulo,
            "autor": autor,
            "genero": genero,
            "estado": estado
        })
        flash("Libro agregado exitosamente.")
        return redirect(url_for("mostrar_libros"))

    return render_template("formulario_libro.html", libro=None)

@app.route("/editar/<id_libro>", methods=["GET", "POST"])
def editar_libro(id_libro):
    clave = f"libro:{id_libro}"
    if not db.exists(clave):
        flash("Libro no encontrado.")
        return redirect(url_for("mostrar_libros"))

    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        autor = request.form["autor"].strip()
        genero = request.form["genero"].strip()
        estado = request.form["estado"]

        if not titulo or not autor or not genero:
            flash("Todos los campos son obligatorios.")
            return redirect(url_for("editar_libro", id_libro=id_libro))

        db.hset(clave, mapping={
            "titulo": titulo,
            "autor": autor,
            "genero": genero,
            "estado": estado
        })
        flash("Libro actualizado correctamente.")
        return redirect(url_for("mostrar_libros"))

    libro = db.hgetall(clave)
    libro["id"] = id_libro
    return render_template("formulario_libro.html", libro=libro)

@app.route("/eliminar/<id_libro>", methods=["GET", "POST"])
def confirmar_eliminacion(id_libro):
    clave = f"libro:{id_libro}"
    if not db.exists(clave):
        flash("Libro no encontrado.")
        return redirect(url_for("mostrar_libros"))

    if request.method == "POST":
        db.delete(clave)
        flash("Libro eliminado correctamente.")
        return redirect(url_for("mostrar_libros"))

    libro = db.hgetall(clave)
    return render_template("confirmar_eliminacion.html", libro=libro)

@app.route("/buscar", methods=["GET", "POST"])
def buscar_libros():
    resultados = None
    if request.method == "POST":
        campo = request.form["campo"]
        valor = request.form["valor"].strip().lower()
        resultados = []

        for libro in obtener_libros():
            if valor in libro[campo].lower():
                resultados.append(libro)

    return render_template("buscar_libros.html", resultados=resultados)

if __name__ == "__main__":
    app.run(debug=True)
