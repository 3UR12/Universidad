from db import conectar_db

# Registra un nuevo artículo en la base de datos
def registrar_articulo(nombre, categoria, cantidad, precio_unitario, descripcion):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO articulos (nombre, categoria, cantidad, precio_unitario, descripcion)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, categoria, cantidad, precio_unitario, descripcion))
    conexion.commit()
    conexion.close()

# Busca artículos por nombre o categoría
def buscar_articulos(filtro, valor):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute(f"""
        SELECT * FROM articulos WHERE {filtro} LIKE ?
    """, ('%' + valor + '%',))
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

# Edita un artículo existente por ID
def editar_articulo(id_articulo, campo, nuevo_valor):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute(f"""
        UPDATE articulos SET {campo} = ? WHERE id = ?
    """, (nuevo_valor, id_articulo))
    conexion.commit()
    conexion.close()

# Elimina un artículo por ID
def eliminar_articulo(id_articulo):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM articulos WHERE id = ?", (id_articulo,))
    conexion.commit()
    conexion.close()

# Lista todos los artículos registrados
def listar_articulos():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM articulos")
    articulos = cursor.fetchall()
    conexion.close()
    return articulos
