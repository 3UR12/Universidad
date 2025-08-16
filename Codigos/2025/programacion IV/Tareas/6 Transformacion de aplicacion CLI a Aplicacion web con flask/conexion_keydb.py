import redis
from config import ConfiguracionAplicacion

def obtener_conexion_keydb():
    """
    Retorna una conexión activa con KeyDB usando redis-py.
    """
    try:
        conexion = redis.Redis(
            host=ConfiguracionAplicacion.KEYDB_HOST,
            port=ConfiguracionAplicacion.KEYDB_PORT,
            password=ConfiguracionAplicacion.KEYDB_PASSWORD,
            decode_responses=True
        )
        conexion.ping()  # Verifica conexión
        return conexion
    except redis.exceptions.ConnectionError:
        return None
