from database import Session, engine
from models import Libro, Base, EstadoLectura

# Crear tablas si no existen
Base.metadata.create_all(engine)

def agregar_libro():
    session = Session()
    try:
        titulo = input("Título: ")
        autor = input("Autor: ")
        genero = input("Género: ")
        estado = input("Estado de lectura (leído/no leído): ")
        libro = Libro(
            titulo=titulo,
            autor=autor,
            genero=genero,
            estado_lectura=EstadoLectura.leido if estado == "leído" else EstadoLectura.no_leido
        )
        session.add(libro)
        session.commit()
        print("✅ Libro agregado.")
    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

def actualizar_libro():
    session = Session()
    try:
        id_libro = int(input("ID del libro a actualizar: "))
        libro = session.get(Libro, id_libro)
        if libro:
            libro.titulo = input("Nuevo título: ")
            libro.autor = input("Nuevo autor: ")
            libro.genero = input("Nuevo género: ")
            estado = input("Nuevo estado (leído/no leído): ")
            libro.estado_lectura = EstadoLectura.leido if estado == "leído" else EstadoLectura.no_leido
            session.commit()
            print("✅ Libro actualizado.")
        else:
            print("⚠️ Libro no encontrado.")
    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

def eliminar_libro():
    session = Session()
    try:
        id_libro = int(input("ID del libro a eliminar: "))
        libro = session.get(Libro, id_libro)
        if libro:
            session.delete(libro)
            session.commit()
            print("🗑️ Libro eliminado.")
        else:
            print("⚠️ Libro no encontrado.")
    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

def ver_libros():
    session = Session()
    try:
        libros = session.query(Libro).all()
        print("\n Listado de libros:")
        for l in libros:
            print(f"ID: {l.id} | Título: {l.titulo} | Autor: {l.autor} | Género: {l.genero} | Estado: {l.estado_lectura.value}")
        print()
    finally:
        session.close()

def buscar_libros():
    session = Session()
    try:
        criterio = input("Buscar por título, autor o género: ")
        resultados = session.query(Libro).filter(
            (Libro.titulo.like(f"%{criterio}%")) |
            (Libro.autor.like(f"%{criterio}%")) |
            (Libro.genero.like(f"%{criterio}%"))
        ).all()
        print("\n🔍 Resultados:")
        for l in resultados:
            print(f"ID: {l.id} | Título: {l.titulo} | Autor: {l.autor} | Género: {l.genero} | Estado: {l.estado_lectura.value}")
        print()
    finally:
        session.close()

def mostrar_menu():
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
            agregar_libro()
        elif opcion == "2":
            actualizar_libro()
        elif opcion == "3":
            eliminar_libro()
        elif opcion == "4":
            ver_libros()
        elif opcion == "5":
            buscar_libros()
        elif opcion == "6":
            print("Programa finalizado.")
            break
        else:
            print("⚠️ Opción no válida.")

if __name__ == "__main__":
    mostrar_menu()
