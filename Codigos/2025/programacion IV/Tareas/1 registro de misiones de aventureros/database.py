import sqlite3

# Conexión a la base de datos SQLite (se crea si no existe)
conexion = sqlite3.connect("aventuras.db")
cursor = conexion.cursor()

# ============================================
# Tabla: heroes
# Información de cada héroe del gremio
# ============================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS heroes (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    clase TEXT CHECK(clase IN ('Guerrero', 'Mago', 'Arquero', 'Ladrón', 'Clérigo')),
    nivel_experiencia INTEGER CHECK(nivel_experiencia >= 0)
)
""")

# ============================================
# Tabla: misiones
# Detalles de cada misión registrada
# ============================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS misiones (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    dificultad INTEGER CHECK(dificultad BETWEEN 1 AND 10),
    localizacion TEXT NOT NULL,
    recompensa INTEGER CHECK(recompensa >= 0)
)
""")

# ============================================
# Tabla: monstruos
# Información de cada monstruo enfrentado
# ============================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS monstruos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    tipo TEXT CHECK(tipo IN ('Dragón', 'Goblin', 'No-muerto', 'Bestia', 'Demonio')),
    nivel_amenaza INTEGER CHECK(nivel_amenaza BETWEEN 1 AND 10)
)
""")

# ============================================
# Tabla: misiones_heroes
# Relación muchos-a-muchos entre héroes y misiones
# ============================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS misiones_heroes (
    id INTEGER PRIMARY KEY,
    id_heroe INTEGER NOT NULL,
    id_mision INTEGER NOT NULL,
    FOREIGN KEY (id_heroe) REFERENCES heroes(id),
    FOREIGN KEY (id_mision) REFERENCES misiones(id)
)
""")

# ============================================
# Tabla: misiones_monstruos
# Relación muchos-a-muchos entre monstruos y misiones
# ============================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS misiones_monstruos (
    id INTEGER PRIMARY KEY,
    id_monstruo INTEGER NOT NULL,
    id_mision INTEGER NOT NULL,
    FOREIGN KEY (id_monstruo) REFERENCES monstruos(id),
    FOREIGN KEY (id_mision) REFERENCES misiones(id)
)
""")

# Guardar cambios y cerrar conexión
conexion.commit()
conexion.close()
