import sqlite3

# ============================================
# Función: conectar_base_datos
# Crea la base de datos y la tabla si no existen
# ============================================
def conectar_base_datos():
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS libros (
        id INTEGER PRIMARY KEY,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        genero TEXT NOT NULL,
        estado_lectura TEXT CHECK(estado_lectura IN ('leído', 'no leído')) NOT NULL
    )
    """)
    conexion.commit()
    return conexion

# ============================================
# Función: agregar_libro
# Añade un nuevo libro a la base de datos
# ============================================
def agregar_libro(conexion):
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado de lectura (leído/no leído): ")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO libros (titulo, autor, genero, estado_lectura) VALUES (?, ?, ?, ?)",
                   (titulo, autor, genero, estado))
    conexion.commit()
    print(" Libro agregado correctamente.")

# ============================================
# Función: actualizar_libro
# Modifica los datos de un libro existente
# ============================================
def actualizar_libro(conexion):
    id_libro = input("ID del libro a actualizar: ")
    nuevo_titulo = input("Nuevo título: ")
    nuevo_autor = input("Nuevo autor: ")
    nuevo_genero = input("Nuevo género: ")
    nuevo_estado = input("Nuevo estado de lectura (leído/no leído): ")
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE libros
        SET titulo = ?, autor = ?, genero = ?, estado_lectura = ?
        WHERE id = ?
    """, (nuevo_titulo, nuevo_autor, nuevo_genero, nuevo_estado, id_libro))
    conexion.commit()
    print(" Libro actualizado correctamente.")

# ============================================
# Función: eliminar_libro
# Elimina un libro por su ID
# ============================================
def eliminar_libro(conexion):
    id_libro = input("ID del libro a eliminar: ")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
    conexion.commit()
    print(" Libro eliminado correctamente.")

# ============================================
# Función: ver_libros
# Muestra todos los libros registrados
# ============================================
def ver_libros(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    print("\n Listado de libros:")
    for libro in libros:
        print(f"ID: {libro[0]} | Título: {libro[1]} | Autor: {libro[2]} | Género: {libro[3]} | Estado: {libro[4]}")
    print()

# ============================================
# Función: buscar_libros
# Busca libros por título, autor o género
# ============================================
def buscar_libros(conexion):
    criterio = input("Buscar por título, autor o género: ")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM libros
        WHERE titulo LIKE ? OR autor LIKE ? OR genero LIKE ?
    """, (f"%{criterio}%", f"%{criterio}%", f"%{criterio}%"))
    resultados = cursor.fetchall()
    print("\n Resultados de búsqueda:")
    for libro in resultados:
        print(f"ID: {libro[0]} | Título: {libro[1]} | Autor: {libro[2]} | Género: {libro[3]} | Estado: {libro[4]}")
    print()

# ============================================
# Función: mostrar_menu
# Muestra el menú interactivo y gestiona opciones
# ============================================
def mostrar_menu():
    conexion = conectar_base_datos()
    while True:
        print(" Menú Biblioteca")
        print("1. Agregar nuevo libro")
        print("2. Actualizar información de un libro")
        print("3. Eliminar libro existente")
        print("4. Ver listado de libros")
        print("5. Buscar libros")
        print("6. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            agregar_libro(conexion)
        elif opcion == "2":
            actualizar_libro(conexion)
        elif opcion == "3":
            eliminar_libro(conexion)
        elif opcion == "4":
            ver_libros(conexion)
        elif opcion == "5":
            buscar_libros(conexion)
        elif opcion == "6":
            print(" Programa finalizado.")
            break
        else:
            print("⚠️ Opción no válida. Intenta de nuevo.")

    conexion.close()

# ============================================meaw
if __name__ == "__main__":
    mostrar_menu()
