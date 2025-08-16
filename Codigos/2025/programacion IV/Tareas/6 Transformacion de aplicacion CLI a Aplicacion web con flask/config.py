import os
from dotenv import load_dotenv

# Carga las variables de entorno
load_dotenv()

# Configuración de Flask y KeyDB
class ConfiguracionAplicacion:
    SECRET_KEY = "clave_secreta_para_flask"
    KEYDB_HOST = os.getenv("KEYDB_HOST")
    KEYDB_PORT = int(os.getenv("KEYDB_PORT"))
    KEYDB_PASSWORD = os.getenv("KEYDB_PASSWORD")
