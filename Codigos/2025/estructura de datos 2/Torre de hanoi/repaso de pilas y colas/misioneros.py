from collections import deque

def es_valido(estado):
    """Comprueba que no haya más caníbales que misioneros en una orilla con misioneros presentes."""
    M_izq, C_izq, M_der, C_der, _ = estado
    return (M_izq == 0 or M_izq >= C_izq) and (M_der == 0 or M_der >= C_der)

def generar_vecinos(estado):
    M_izq, C_izq, M_der, C_der, bote = estado
    movimientos = [(2,0), (0,2), (1,1), (1,0), (0,1)]
    vecinos = []

    for m, c in movimientos:
        if bote == "izq":
            if M_izq >= m and C_izq >= c:
                nuevo = (M_izq - m, C_izq - c, M_der + m, C_der + c, "der")
                if es_valido(nuevo):
                    vecinos.append(nuevo)
        else:
            if M_der >= m and C_der >= c:
                nuevo = (M_izq + m, C_izq + c, M_der - m, C_der - c, "izq")
                if es_valido(nuevo):
                    vecinos.append(nuevo)
    return vecinos

def bfs_solucion():
    inicio = (3, 3, 0, 0, "izq")
    objetivo = (0, 0, 3, 3, "der")
    cola = deque([[inicio]])
    visitados = {inicio}

    while cola:
        camino = cola.popleft()
        estado_actual = camino[-1]
        if estado_actual == objetivo:
            return camino
        for vecino in generar_vecinos(estado_actual):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(camino + [vecino])
    return None

if __name__ == "__main__":
    solucion = bfs_solucion()
    print("Secuencia (M_izq, C_izq, M_der, C_der, bote):")
    for paso in solucion:
        print(paso)
