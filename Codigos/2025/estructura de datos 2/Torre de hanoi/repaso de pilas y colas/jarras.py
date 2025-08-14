from collections import deque

def estado_vecinos(estado):
    """Genera los estados vecinos aplicando las reglas del problema."""
    j4, j3 = estado
    capacidad_j4, capacidad_j3 = 4, 3
    vecinos = []

    # Llenar jarra 4
    vecinos.append((capacidad_j4, j3))
    # Llenar jarra 3
    vecinos.append((j4, capacidad_j3))
    # Vaciar jarra 4
    vecinos.append((0, j3))
    # Vaciar jarra 3
    vecinos.append((j4, 0))
    # Verter de jarra 4 a jarra 3
    transfer = min(j4, capacidad_j3 - j3)
    vecinos.append((j4 - transfer, j3 + transfer))
    # Verter de jarra 3 a jarra 4
    transfer = min(j3, capacidad_j4 - j4)
    vecinos.append((j4 + transfer, j3 - transfer))

    return vecinos

def bfs_solucion():
    inicio = (0, 0)
    objetivo = (2, 0)
    cola = deque([[inicio]])
    visitados = {inicio}

    while cola:
        camino = cola.popleft()
        estado_actual = camino[-1]
        if estado_actual == objetivo:
            return camino
        for vecino in estado_vecinos(estado_actual):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(camino + [vecino])
    return None

if __name__ == "__main__":
    solucion = bfs_solucion()
    print("Secuencia de pasos (J4, J3):")
    for paso in solucion:
        print(paso)
