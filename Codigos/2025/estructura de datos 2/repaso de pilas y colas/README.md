## 📚 Resolución de Problemas de Lógica y Programación

Este documento describe el análisis y la solución a tres problemas clásicos de lógica y programación.  
Se incluye el razonamiento, el método utilizado, la secuencia de pasos, diagramas de estados y análisis de complejidad.

---

## 1️⃣ Problema de las jarras (4 galones y 3 galones)

**Enunciado:**  
Dispones de una jarra de 4 galones y otra de 3 galones, sin marcas de medición, y una fuente ilimitada de agua.  
Objetivo: Obtener exactamente **2 galones** en la jarra de 4 galones.

**Metodología:**  
- Representar el problema como un grafo de estados `(J4, J3)` donde `J4` y `J3` indican litros actuales en cada jarra.  
- Usar **Búsqueda en Anchura (BFS)** para encontrar la secuencia mínima de pasos.  
- Operaciones posibles: llenar, vaciar y verter entre jarras.

**Solución mínima:**
```
(0,0) → (0,3) → (3,0) → (3,3) → (4,2) → (0,2) → (2,0)
```

**Diagrama simplificado de estados** (cada nodo = (J4,J3)):
```
(0,0) → (0,3) → (3,0) → (3,3) 
                          ↓
                        (4,2) → (0,2) → (2,0)
```

**Complejidad:**  
- Estados posibles: 20 combinaciones.  
- BFS: tiempo **O(V+E)**, con `V ≤ 20`.

---

## 2️⃣ Problema de los misioneros y caníbales

**Enunciado:**  
Tres misioneros y tres caníbales deben cruzar un río usando una barca con capacidad máxima de dos personas.  
Restricción: En ninguna orilla puede haber más caníbales que misioneros si hay al menos un misionero en esa orilla.

**Metodología:**  
- Estado: `(M_izq, C_izq, M_der, C_der, bote)` donde *bote* ∈ {I, D}.  
- Movimientos: `(2,0)`, `(0,2)`, `(1,1)`, `(1,0)`, `(0,1)`.  
- Filtrar solo estados seguros.  
- Usar BFS para encontrar el mínimo número de cruces.

**Secuencia válida mínima (11 cruces):**
1. (3,3,0,0,I) → (2,2,1,1,D)  [1M,1C →]  
2. (2,2,1,1,D) → (3,2,0,1,I)  [1M ←]  
3. (3,2,0,1,I) → (3,0,0,3,D)  [2C →]  
4. (3,0,0,3,D) → (3,1,0,2,I)  [1C ←]  
5. (3,1,0,2,I) → (1,1,2,2,D)  [2M →]  
6. (1,1,2,2,D) → (2,2,1,1,I)  [1M,1C ←]  
7. (2,2,1,1,I) → (2,0,1,3,D)  [2C →]  
8. (2,0,1,3,D) → (2,1,1,2,I)  [1C ←]  
9. (2,1,1,2,I) → (0,1,3,2,D)  [2M →]  
10. (0,1,3,2,D) → (1,1,2,2,I) [1M ←]  
11. (1,1,2,2,I) → (0,0,3,3,D) [1M,1C →] 

```
(3,3,0,0,I)
   |(1M,1C) →
(2,2,1,1,D)
   |(1M) ←
(3,2,0,1,I)
   |(0M,2C) →
(3,0,0,3,D)
   |(0M,1C) ←
(3,1,0,2,I)
   |(2M,0C) →
(1,1,2,2,D)
   |(1M,1C) ←
(2,2,1,1,I)
   |(0M,2C) →
(2,0,1,3,D)
   |(0M,1C) ←
(2,1,1,2,I)
   |(2M,0C) →
(0,1,3,2,D)
   |(1M) ←
(1,1,2,2,I)
   |(1M,1C) →
(0,0,3,3,D)
```
*(Cada flecha indica quién cruza, en formato `(misioneros, caníbales)`; el último estado es el objetivo.)*

**Complejidad:**  
- Espacio de estados: hasta 32 combinaciones crudas (menos al filtrar).  
- BFS: garantiza la mínima cantidad de cruces.

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
- `TEST(i)` verdadero → imprime `i` inmediatamente.  
- `TEST(i)` falso → apila `i` para imprimirlo después.  
- Al final, los rechazados se imprimen en orden inverso (LIFO).

**Ejemplo con N=3:**
- Si `TEST(i)` siempre es verdadero → `1 2 3`  
- Si solo falla en `i=2` → `1 3 2`  
- Si solo `i=3` es verdadero → `3 2 1`

**Opciones posibles del enunciado:**  
- **Posibles:** a) 1 2 3 b) 1 3 2 e) 2 3 1 f) 3 2 1  
- **No posibles:** c) 2 1 3 d) 3 1 2

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

**Autor:** 3UR12 – Desarrollo y análisis en Python a partir de problemas clásicos de lógica.

