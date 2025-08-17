# Simula datos por provincia basados en el año
def simular_por_provincia(datos, nombre_provincia):
    provincias = ["Panamá", "Colón", "Chiriquí", "Veraguas", "Coclé"]
    if nombre_provincia not in provincias:
        return None

    # Distribuye el porcentaje con una variación aleatoria controlada
    datos_simulados = []
    for registro in datos:
        variacion = hash(nombre_provincia + str(registro["año"])) % 5  # Simula variación
        porcentaje = max(0, registro["porcentaje"] - variacion)
        datos_simulados.append({
            "provincia": nombre_provincia,
            "año": registro["año"],
            "porcentaje": porcentaje
        })
    return datos_simulados
