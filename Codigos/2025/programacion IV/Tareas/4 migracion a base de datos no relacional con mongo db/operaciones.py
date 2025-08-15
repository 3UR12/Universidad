from database import libros_collection
from bson.objectid import ObjectId

def agregar_libro(titulo, autor, genero, estado):
    libro = {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }
    result = libros_collection.insert_one(libro)
    return str(result.inserted_id)

def actualizar_libro(libro_id, campo, nuevo_valor):
    result = libros_collection.update_one(
        {"_id": ObjectId(libro_id)},
        {"$set": {campo: nuevo_valor}}
    )
    return result.modified_count

def eliminar_libro(libro_id):
    result = libros_collection.delete_one({"_id": ObjectId(libro_id)})
    return result.deleted_count

def listar_libros():
    return list(libros_collection.find())

def buscar_libros(campo, valor):
    filtro = {campo: {"$regex": valor, "$options": "i"}}
    return list(libros_collection.find(filtro))
