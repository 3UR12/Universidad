from db import crear_tabla_articulos
from articulo import (
    registrar_articulo, buscar_articulos, editar_articulo,
    eliminar_articulo, listar_articulos
)
from utils import validar_no_vacio, validar_entero, validar_decimal

# Muestra el menú principal
def mostrar_menu():
    print("\n Menú de Gestión de Artículos")
    print("1. Registrar nuevo artículo")
    print("2. Buscar artículos")
    print("3. Editar artículo")
    print("4. Eliminar artículo")
    print("5. Mostrar todos los artículos")
    print("6. Salir")

# Ejecuta la aplicación
def ejecutar_app():
    crear_tabla_articulos()
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            # Registro de artículo
            nombre = input("Nombre: ")
            categoria = input("Categoría: ")
            cantidad = input("Cantidad: ")
            precio = input("Precio unitario: ")
            descripcion = input("Descripción: ")

            if not (validar_no_vacio(nombre) and validar_no_vacio(categoria) and
                    validar_entero(cantidad) and validar_decimal(precio)):
                print("❌ Error: Verifica los campos ingresados.")
                continue

            registrar_articulo(nombre, categoria, int(cantidad), float(precio), descripcion)
            print(" Artículo registrado correctamente.")

        elif opcion == "2":
            # Búsqueda
            filtro = input("Buscar por (nombre/categoria): ").lower()
            valor = input("Valor a buscar: ")
            resultados = buscar_articulos(filtro, valor)
            for art in resultados:
                print(art)

        elif opcion == "3":
            # Edición
            id_articulo = input("ID del artículo a editar: ")
            campo = input("Campo a editar (nombre, categoria, cantidad, precio_unitario, descripcion): ")
            nuevo_valor = input("Nuevo valor: ")
            editar_articulo(int(id_articulo), campo, nuevo_valor)
            print(" Artículo actualizado.")

        elif opcion == "4":
            # Eliminación
            id_articulo = input("ID del artículo a eliminar: ")
            eliminar_articulo(int(id_articulo))
            print("🗑️ Artículo eliminado.")

        elif opcion == "5":
            # Listado
            articulos = listar_articulos()
            print("\n Artículos registrados:")
            for art in articulos:
                print(f"ID: {art[0]} | Nombre: {art[1]} | Categoría: {art[2]} | Cantidad: {art[3]} | Precio: {art[4]} | Descripción: {art[5]}")

        elif opcion == "6":
            print(" Saliendo del sistema...")
            break
        else:
            print("❌ Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    ejecutar_app()
