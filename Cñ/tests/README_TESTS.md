# Documentación de Tests - Lenguaje Cñ

## Tests Disponibles

Esta carpeta contiene los tests más representativos para verificar todas las funcionalidades del lenguaje Cñ. Cada archivo `.txt` puede ser cargado y ejecutado desde la interfaz gráfica.

### 📊 **Análisis Estadísticos**

#### `test_estadisticas_basico.txt`
**Funcionalidad:** Análisis estadístico básico con método `promedio()`
**Descripción:** 
- Declara un array de enteros con 5 calificaciones de estudiantes
- Calcula el promedio usando `Estadisticas.promedio(datos)`
- Demuestra el uso de métodos estáticos y manejo de arrays
**Resultado esperado:** 30.0 (promedio de [10, 20, 30, 40, 50])
**Conceptos:** Clases estáticas, arrays, análisis estadístico

---

### 🔢 **Manejo de Arrays**

#### `test_array_fibonacci.txt`
**Funcionalidad:** Generación de secuencia Fibonacci con arrays
**Descripción:**
- Utiliza un array para almacenar los primeros números de Fibonacci
- Demuestra inicialización manual y cálculos iterativos
- Muestra acceso y asignación de elementos de array
**Conceptos:** Arrays, bucles, asignación de elementos

#### `test_array_max.txt`
**Funcionalidad:** Búsqueda del elemento máximo en un array
**Descripción:**
- Recorre un array para encontrar el valor máximo
- Utiliza bucles `para` y comparaciones condicionales
- Demuestra algoritmo básico de búsqueda
**Conceptos:** Arrays, bucles `para`, condicionales

#### `test_array_sort.txt`
**Funcionalidad:** Algoritmo de ordenamiento burbuja
**Descripción:**
- Implementa ordenamiento burbuja para arrays de enteros
- Utiliza bucles anidados y intercambio de elementos
- Demuestra algoritmo de ordenamiento completo
**Conceptos:** Arrays, bucles anidados, algoritmos de ordenamiento

---

### 🔁 **Estructuras de Control**

#### `test_for.txt`
**Funcionalidad:** Bucle `para` básico
**Descripción:**
- Demuestra la sintaxis del bucle `para` en Cñ
- Realiza suma acumulativa de números del 1 al 10
- Muestra declaración de variables y operaciones aritméticas
**Resultado esperado:** 55 (suma de 1 a 10)
**Conceptos:** Bucle `para`, variables, operaciones aritméticas

#### `test_for_factorial.txt`
**Funcionalidad:** Cálculo de factorial usando bucle `para`
**Descripción:**
- Calcula el factorial de un número (5!) usando iteración
- Demuestra bucle con decremento y multiplicación acumulativa
- Muestra uso práctico de bucles en algoritmos matemáticos
**Resultado esperado:** 120 (5! = 5×4×3×2×1)
**Conceptos:** Bucle `para`, factorial, algoritmos matemáticos

---

### 🔢 **Tipos de Datos Numéricos**

#### `test_real_basico.txt`
**Funcionalidad:** Operaciones con números reales (float)
**Descripción:**
- Declara variables de tipo `real` (flotantes)
- Realiza operaciones aritméticas con decimales
- Demuestra precisión de punto flotante
**Conceptos:** Tipo `real`, operaciones con decimales

#### `test_mixto_entero_real.txt`
**Funcionalidad:** Operaciones mixtas entre enteros y reales
**Descripción:**
- Combina operaciones entre tipos `entero` y `real`
- Demuestra conversión automática de tipos
- Muestra resultado en punto flotante para mayor precisión
**Conceptos:** Tipos mixtos, conversión automática, precisión numérica

#### `test_division_entera.txt`
**Funcionalidad:** División entera vs división real
**Descripción:**
- Compara comportamiento de división entre enteros vs reales
- Demuestra cuando el resultado es entero vs decimal
- Muestra reglas de tipos en operaciones aritméticas
**Conceptos:** División entera, división real, tipos de resultado

---

## Cómo Usar los Tests

1. **Desde la GUI:**
   - Ejecutar `gui.py`
   - Hacer clic en "Cargar Archivo"
   - Seleccionar cualquier archivo `.txt` de esta carpeta
   - Hacer clic en "Analizar" para ver tokens, parsing y resultado

2. **Verificación:**
   - **Análisis Léxico:** Muestra todos los tokens identificados
   - **Análisis Sintáctico:** "Aceptado" si la sintaxis es correcta
   - **Output:** Resultado de la ejecución del programa

3. **Solución de Problemas:**
   - Si aparece "Rechazado": Error de sintaxis en el código
   - Si aparece "Error" en Output: Error durante la ejecución
   - Verificar que los arrays estén inicializados correctamente

## Orden Sugerido para Pruebas

1. **Básico:** `test_for.txt` - Estructura de control simple
2. **Arrays:** `test_array_max.txt` - Manejo básico de arrays  
3. **Algoritmos:** `test_array_sort.txt` - Algoritmo más complejo
4. **Tipos:** `test_real_basico.txt` - Números decimales
5. **Mixto:** `test_mixto_entero_real.txt` - Combinación de tipos
6. **Avanzado:** `test_estadisticas_basico.txt` - Análisis estadístico

Cada test está diseñado para ser independiente y demostrar conceptos específicos del lenguaje Cñ.
