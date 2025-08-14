def TEST(x):
    # Cambia esta condición para simular distintos casos
    return x % 2 == 1  # Verdadero para impares

def main():
    N = 3
    pila = []

    for i in range(1, N + 1):
        if TEST(i):
            print(i, end=" ")
        else:
            pila.append(i)

    while pila:
        print(pila.pop(), end=" ")

if __name__ == "__main__":
    main()
