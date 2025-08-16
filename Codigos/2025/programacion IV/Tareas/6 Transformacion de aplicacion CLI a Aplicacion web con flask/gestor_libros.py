import json
from utils import generar_id_unico

CLAVE_LIBRO = "libro:"

def guardar_libro(conexion, titulo, autor, genero, estado):
    """
    Guarda un nuevo libro en KeyDB.
    """
    id_libro = generar_id_unico()
    datos_libro = {
        "id": id_libro,
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }
    conexion.set(CLAVE_LIBRO + id_libro, json.dumps(datos_libro))
    return id_libro

def obtener_libro_por_id(conexion, id_libro):
    """
    Obtiene los datos de un libro por su ID.
    """
    datos = conexion.get(CLAVE_LIBRO + id_libro)
    if datos:
        return json.loads(datos)
    return None

def actualizar_libro(conexion, id_libro, titulo, autor, genero, estado):
    """
    Actualiza los datos de un libro existente.
    """
    libro = {
        "id": id_libro,
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }
    conexion.set(CLAVE_LIBRO + id_libro, json.dumps(libro))

def eliminar_libro(conexion, id_libro):
    """
    Elimina un libro por su ID.
    """
    conexion.delete(CLAVE_LIBRO + id_libro)

def obtener_todos_los_libros(conexion):
    """
    Retorna todos los libros registrados.
    """
    libros = []
    for clave in conexion.scan_iter(CLAVE_LIBRO + "*"):
        datos = conexion.get(clave)
        libros.append(json.loads(datos))
    return libros

def buscar_libros_por_campo(conexion, campo, valor):
    """
    Busca libros por título, autor o género.
    """
    resultados = []
    for clave in conexion.scan_iter(CLAVE_LIBRO + "*"):
        datos = conexion.get(clave)
        libro = json.loads(datos)
        if libro.get(campo, "").lower() == valor.lower():
            resultados.append(libro)
    return resultados
