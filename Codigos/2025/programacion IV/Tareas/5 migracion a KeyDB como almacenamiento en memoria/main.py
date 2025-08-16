from conexion_keydb import obtener_conexion_keydb
from gestor_libros import (
    agregar_libro,
    actualizar_libro,
    eliminar_libro,
    ver_libros,
    buscar_libros
)

def mostrar_menu():
    """
    Muestra el menú principal de opciones.
    """
    print("\n--- Biblioteca Personal ---")
    print("1. Agregar nuevo libro")
    print("2. Actualizar información de un libro")
    print("3. Eliminar libro existente")
    print("4. Ver listado de libros")
    print("5. Buscar libros")
    print("6. Salir")

def ejecutar_aplicacion():
    """
    Ejecuta el ciclo principal de la aplicación.
    """
    conexion = obtener_conexion_keydb()
    if not conexion:
        return

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            genero = input("Género: ")
            estado = input("Estado de lectura: ")
            agregar_libro(conexion, titulo, autor, genero, estado)

        elif opcion == "2":
            id_libro = input("ID del libro: ")
            campo = input("Campo a modificar (titulo, autor, genero, estado): ")
            nuevo_valor = input("Nuevo valor: ")
            actualizar_libro(conexion, id_libro, campo, nuevo_valor)

        elif opcion == "3":
            id_libro = input("ID del libro a eliminar: ")
            eliminar_libro(conexion, id_libro)

        elif opcion == "4":
            ver_libros(conexion)

        elif opcion == "5":
            campo = input("Buscar por (titulo, autor, genero): ")
            valor = input("Valor a buscar: ")
            buscar_libros(conexion, campo, valor)

        elif opcion == "6":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    ejecutar_aplicacion()
