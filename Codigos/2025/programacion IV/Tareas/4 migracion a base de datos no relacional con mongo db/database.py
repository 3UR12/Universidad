from pymongo import MongoClient
import os

# Variables de entorno para Docker
usuario = os.getenv("MONGO_INITDB_ROOT_USERNAME", "admin")
contraseña = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "admin321")
host = os.getenv("MONGO_HOST", "localhost")
puerto = os.getenv("MONGO_PORT", "27017")

# Cadena de conexión
uri = f"mongodb://{usuario}:{contraseña}@{host}:{puerto}/"

try:
    cliente = MongoClient(uri, serverSelectionTimeoutMS=3000)
    cliente.server_info()  # Verifica conexión
    db = cliente["biblioteca_db"]
    libros_collection = db["libros"]
except Exception as e:
    print("❌ Error de conexión a MongoDB:", e)
    libros_collection = None
