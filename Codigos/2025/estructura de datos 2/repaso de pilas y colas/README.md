## 📚 Resolución de Problemas de Lógica y Programación

Este documento describe el análisis y la solución a tres problemas clásicos de lógica y programación.  
Se incluye el razonamiento, el método utilizado, la secuencia de pasos, diagramas de estados y análisis de complejidad.

---

## 1️⃣ Problema de las jarras (4 galones y 3 galones)

mermaid
graph TD
    A["Estado Inicial: (0,0)"] --> B["Llenar jarra de 4L: (4,0)"]
    B --> C["Verter 4L en jarra de 3L: (1,3)"]
    C --> D["Vaciar jarra 3L: (1,0)"]
    D --> E["Verter jarra 4L a 3L: (0,1)"]
    E --> F["Llenar jarra de 4L: (4,1)"]
    F --> G["Verter hasta llenar jarra 3L: (2,3) → ¡Meta!"]


**Enunciado:**  
Dispones de una jarra de 4 galones y otra de 3 galones, sin marcas de medición, y una fuente ilimitada de agua.  
Objetivo: Obtener exactamente **2 galones** en la jarra de 4 galones.

**Metodología:**  
- Representar el problema como un grafo de estados `(J4, J3)` donde `J4` y `J3` indican litros actuales.
- Usar **Búsqueda en Anchura (BFS)** para encontrar la secuencia mínima de pasos.
- Operaciones posibles: llenar, vaciar y verter entre jarras.

**Solución mínima:**
```
(0,0) → (0,3) → (3,0) → (3,3) → (4,2) → (0,2) → (2,0) ✅
```

**Diagrama simplificado de estados** (cada nodo = (J4,J3)):

```
(0,0) → (0,3) → (3,0) → (3,3) 
                          ↓
                        (4,2) → (0,2) → (2,0)
```

**Complejidad:**  
- Estados posibles: 20 combinaciones.
- BFS: tiempo O(E) con E = número de transiciones.

---

## 2️⃣ Problema de los misioneros y caníbales

**Enunciado:**  
Tres misioneros y tres caníbales deben cruzar un río usando una barca con capacidad máxima de dos personas.  
Restricción: En ninguna orilla puede haber más caníbales que misioneros si hay al menos un misionero en esa orilla.

**Metodología:**  
- Estado: `(M_izq, C_izq, M_der, C_der, bote)`.
- Movimientos: `(2,0)`, `(0,2)`, `(1,1)`, `(1,0)`, `(0,1)`.
- Filtrar solo estados seguros.
- BFS para encontrar mínimo número de cruces.

**Secuencia mínima (7 pasos):**
1. (3,3,0,0,I) → (3,1,0,2,D)
2. (3,1,0,2,D) → (3,2,0,1,I)
3. (3,2,0,1,I) → (1,2,2,1,D)
4. (1,2,2,1,D) → (2,2,1,1,I)
5. (2,2,1,1,I) → (0,2,3,1,D)
6. (0,2,3,1,D) → (0,3,3,0,I)
7. (0,3,3,0,I) → (0,0,3,3,D) ✅

**Diagrama de flujo simplificado:**
```
(3,3,0,0,I)
   |(0,2) caníbales→
(3,1,0,2,D)
   |(0,1) caníbal←
(3,2,0,1,I)
   |(2,0) misioneros→
(1,2,2,1,D)
   |(1,0) misionero←
(2,2,1,1,I)
   |(0,2) caníbales→
(0,2,3,1,D)
   |(0,1) caníbal←
(0,3,3,0,I)
   |(0,2) misioneros→
(0,0,3,3,D)
```
*(Los movimientos están anotados como "(misioneros, caníbales)")*

**Complejidad:**  
Espacio de estados pequeño (~32 estados posibles). BFS es óptimo.

---

## 3️⃣ Análisis del código `TEST` y pila

**Código original en C (resumen):**
```c
for (i = 1; i <= N; i++)
    if (TEST(i))
        printf("%d", i);
    else
        Push(&i, p);

while (!VaciaPila(p)) {
    Tope(&i, p);
    Pop(p);
    printf("%d", i);
}
```

**Comportamiento:**
- `TEST(i)` verdadero: imprime `i` inmediatamente.
- `TEST(i)` falso: apila `i` para imprimirlo después.
- Al final, los elementos rechazados se imprimen en orden inverso (LIFO).

**Ejemplo con N=3:**
- Si `TEST(i)` siempre es verdadero → `1 2 3`  
- Si solo falla en `i=2` → `1 3 2`  
- Si solo `i=3` es verdadero → `3 2 1`

**Diagrama de flujo lógico:**
```
    ┌───────────┐
    │   i=1..N  │
    └─────┬─────┘
          v
     ┌───────────┐
     │ TEST(i)?  │
     └───┬───┬───┘
       sí│   │no
         │   v
         │  push(i)
         v
     print(i)

   [Fin del bucle]

      v
   while pila no vacía:
       print(pop())
```

**Conclusión:** La secuencia final está formada por:
1. Valores aceptados (`TEST` verdadero) en orden creciente.
2. Valores rechazados (`TEST` falso) en orden inverso al que aparecieron.

---

## 📂 Archivos del repositorio

- `jarras.py` → Solución al problema de las jarras con BFS.
- `misioneros.py` → Solución a misioneros y caníbales con BFS y restricciones.
- `test_pila.py` → Simulación del código `TEST` y pila.
- `README.md` → Documentación detallada (este archivo).

---

## ▶️ Ejecución

En terminal, dentro de la carpeta del proyecto:
```bash
python jarras.py
python misioneros.py
python test_pila.py
```

---

**Autor: 3UR12** Desarrollo y análisis en Python a partir de problemas clásicos de lógica.






