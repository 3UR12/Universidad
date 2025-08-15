from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configura tu cadena de conexión aquí
DB_USER = "usuario"
DB_PASSWORD = "clave_usuario"
DB_HOST = "localhost"
DB_NAME = "biblioteca_db"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Crea el motor y la sesión
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
