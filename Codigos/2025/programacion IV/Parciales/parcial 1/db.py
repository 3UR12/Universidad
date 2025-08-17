import sqlite3

# Conecta a la base de datos
def conectar_db():
    return sqlite3.connect("presupuesto.db")

# Crea la tabla de artículos si no existe
def crear_tabla_articulos():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            descripcion TEXT
        )
    """)
    conexion.commit()
    conexion.close()
