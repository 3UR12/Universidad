import os
import redis
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

def obtener_conexion_keydb():
    """
    Establece y retorna una conexión con KeyDB usando redis-py.
    """
    try:
        conexion = redis.Redis(
            host=os.getenv("KEYDB_HOST"),
            port=int(os.getenv("KEYDB_PORT")),
            password=os.getenv("KEYDB_PASSWORD"),
            decode_responses=True
        )
        # Verifica la conexión con un ping
        conexion.ping()
        return conexion
    except redis.exceptions.ConnectionError:
        print("Error: No se pudo conectar con KeyDB.")
        return None
