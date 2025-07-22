# Clase Estadisticas - Análisis Estadísticos en Cñ

## Descripción
La clase `Estadisticas` proporciona métodos estáticos para realizar análisis estadísticos sobre arrays de datos numéricos (enteros o reales).

## Métodos Disponibles

### 1. `promedio(datos)`
**Descripción:** Calcula la media aritmética de un conjunto de datos.
**Parámetros:** 
- `datos`: Array de enteros o reales
**Retorna:** Valor real (promedio)
**Ejemplo:**
```cñ
arreglo entero notas[5] = {85, 90, 78, 92, 88};
real media = Estadisticas.promedio(notas); // Resultado: 86.6
```

### 2. `mediana(datos)`  
**Descripción:** Calcula el valor medio cuando los datos están ordenados.
**Parámetros:**
- `datos`: Array de enteros o reales
**Retorna:** Valor real (mediana)
**Ejemplo:**
```cñ
arreglo entero valores[5] = {1, 3, 3, 6, 7};
real mediana = Estadisticas.mediana(valores); // Resultado: 3.0
```

### 3. `moda(datos)`
**Descripción:** Encuentra el valor que aparece con mayor frecuencia.
**Parámetros:**
- `datos`: Array de enteros o reales  
**Retorna:** Valor real (moda)
**Ejemplo:**
```cñ
arreglo entero frecuencias[6] = {1, 2, 2, 3, 2, 4};
real moda = Estadisticas.moda(frecuencias); // Resultado: 2.0
```

### 4. `desviacion_estandar(datos)`
**Descripción:** Mide la dispersión de los datos respecto a la media.
**Parámetros:**
- `datos`: Array de enteros o reales
**Retorna:** Valor real (desviación estándar)
**Ejemplo:**
```cñ
arreglo real temps[4] = {20.5, 21.0, 19.5, 20.0};
real desviacion = Estadisticas.desviacion_estandar(temps);
```

### 5. `minimo(datos)`
**Descripción:** Encuentra el valor mínimo en el conjunto de datos.
**Parámetros:**
- `datos`: Array de enteros o reales
**Retorna:** Valor real (mínimo)
**Ejemplo:**
```cñ
arreglo entero numeros[5] = {15, 3, 9, 21, 7};
real min_val = Estadisticas.minimo(numeros); // Resultado: 3.0
```

### 6. `maximo(datos)`
**Descripción:** Encuentra el valor máximo en el conjunto de datos.
**Parámetros:**
- `datos`: Array de enteros o reales
**Retorna:** Valor real (máximo)
**Ejemplo:**
```cñ
arreglo entero numeros[5] = {15, 3, 9, 21, 7};
real max_val = Estadisticas.maximo(numeros); // Resultado: 21.0
```

### 7. `rango(datos)`
**Descripción:** Calcula la diferencia entre el valor máximo y mínimo.
**Parámetros:**
- `datos`: Array de enteros o reales
**Retorna:** Valor real (rango)
**Ejemplo:**
```cñ
arreglo entero datos[4] = {10, 25, 15, 30};
real rango = Estadisticas.rango(datos); // Resultado: 20.0 (30-10)
```

### 8. `suma(datos)`
**Descripción:** Calcula la suma total de todos los valores.
**Parámetros:**
- `datos`: Array de enteros o reales  
**Retorna:** Valor real (suma)
**Ejemplo:**
```cñ
arreglo entero valores[4] = {5, 10, 15, 20};
real total = Estadisticas.suma(valores); // Resultado: 50.0
```

## Casos de Uso

### Análisis de Calificaciones
```cñ
entero main() {
    arreglo entero calificaciones[8] = {85, 90, 78, 92, 88, 85, 95, 87};
    
    real promedio_clase = Estadisticas.promedio(calificaciones);
    real calificacion_max = Estadisticas.maximo(calificaciones); 
    real calificacion_min = Estadisticas.minimo(calificaciones);
    real mediana_clase = Estadisticas.mediana(calificaciones);
    
    regresa promedio_clase;
}
```

### Análisis de Temperaturas
```cñ
entero main() {
    arreglo real temperaturas[7] = {23.5, 25.0, 22.8, 26.3, 24.1, 25.9, 23.7};
    
    real temp_promedio = Estadisticas.promedio(temperaturas);
    real variabilidad = Estadisticas.desviacion_estandar(temperaturas);
    real amplitud_temp = Estadisticas.rango(temperaturas);
    
    regresa temp_promedio;
}
```

## Notas Importantes

1. Todos los métodos son **estáticos**, se llaman usando `Estadisticas.metodo(datos)`
2. Los métodos aceptan tanto arrays de **enteros** como de **reales**
3. Todos los métodos retornan valores de tipo **real** para mayor precisión
4. Los arrays deben estar previamente declarados e inicializados
5. Los métodos manejan automáticamente la conversión de tipos entre enteros y reales

## Archivos de Prueba

- `test_estadisticas_basico.txt`: Ejemplo representativo que calcula el promedio de un conjunto de datos