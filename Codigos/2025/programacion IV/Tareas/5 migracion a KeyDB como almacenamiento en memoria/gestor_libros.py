import json
from utils import generar_id_unico

# Prefijo para las claves de libros
CLAVE_LIBRO = "libro:"

def agregar_libro(conexion, titulo, autor, genero, estado):
    """
    Agrega un nuevo libro a KeyDB.
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

def actualizar_libro(conexion, id_libro, campo, nuevo_valor):
    """
    Actualiza un campo específico de un libro.
    """
    clave = CLAVE_LIBRO + id_libro
    datos = conexion.get(clave)
    if datos:
        libro = json.loads(datos)
        libro[campo] = nuevo_valor
        conexion.set(clave, json.dumps(libro))
    else:
        print("Libro no encontrado.")

def eliminar_libro(conexion, id_libro):
    """
    Elimina un libro por su ID.
    """
    conexion.delete(CLAVE_LIBRO + id_libro)

def ver_libros(conexion):
    """
    Muestra todos los libros registrados.
    """
    for clave in conexion.scan_iter(CLAVE_LIBRO + "*"):
        datos = conexion.get(clave)
        libro = json.loads(datos)
        print(libro)

def buscar_libros(conexion, campo, valor):
    """
    Busca libros por título, autor o género.
    """
    encontrados = []
    for clave in conexion.scan_iter(CLAVE_LIBRO + "*"):
        datos = conexion.get(clave)
        libro = json.loads(datos)
        if libro.get(campo, "").lower() == valor.lower():
            encontrados.append(libro)
    for libro in encontrados:
        print(libro)
