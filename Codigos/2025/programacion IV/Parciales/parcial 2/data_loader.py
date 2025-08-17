import json

# Carga los datos desde el archivo JSON
def cargar_datos_vacunacion():
    with open("datos/vacunacion.json", "r") as archivo:
        return json.load(archivo)
