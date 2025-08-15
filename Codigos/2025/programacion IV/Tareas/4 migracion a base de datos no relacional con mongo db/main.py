from operaciones import agregar_libro, actualizar_libro, eliminar_libro, listar_libros, buscar_libros

def mostrar_menu():
    print("\n📚 Menú Biblioteca MongoDB")
    print("1. Agregar libro")
    print("2. Actualizar libro")
    print("3. Eliminar libro")
    print("4. Ver libros")
    print("5. Buscar libros")
    print("6. Salir")

def ejecutar():
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            t = input("Título: ")
            a = input("Autor: ")
            g = input("Género: ")
            e = input("Estado: ")
            id = agregar_libro(t, a, g, e)
            print(f"✅ Libro agregado con ID: {id}")
        elif opcion == "2":
            id = input("ID del libro: ")
            campo = input("Campo a actualizar (titulo, autor, genero, estado): ")
            valor = input("Nuevo valor: ")
            if actualizar_libro(id, campo, valor):
                print("✅ Libro actualizado")
            else:
                print("⚠️ No se encontró el libro")
        elif opcion == "3":
            id = input("ID del libro a eliminar: ")
            if eliminar_libro(id):
                print("✅ Libro eliminado")
            else:
                print("⚠️ No se encontró el libro")
        elif opcion == "4":
            libros = listar_libros()
            for l in libros:
                print(f"{l['_id']}: {l['titulo']} - {l['autor']} ({l['genero']}) [{l['estado']}]")
        elif opcion == "5":
            campo = input("Buscar por (titulo, autor, genero): ")
            valor = input("Valor a buscar: ")
            resultados = buscar_libros(campo, valor)
            if resultados:
                for l in resultados:
                    print(f"{l['_id']}: {l['titulo']} - {l['autor']} ({l['genero']}) [{l['estado']}]")
            else:
                print("🔍 No se encontraron resultados")
        elif opcion == "6":
            print(" Saliendo...")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    ejecutar()
