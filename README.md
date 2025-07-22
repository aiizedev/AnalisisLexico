# 🚀 Lenguaje Cñ - Intérprete con Análisis Estadísticos

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.13-green.svg)
![Status](https://img.shields.io/badge/status-estable-success.svg)

## 📖 Descripción

**Cñ** es un lenguaje de programación completo con sintaxis inspirada en C, desarrollado completamente en Python. Incluye análisis léxico, sintáctico, evaluación de código y una interfaz gráfica moderna con tema nocturno. 

### ✨ Características Principales

- 🔤 **Tipos de datos:** `entero`, `real`, `arreglo`
- 🔁 **Estructuras de control:** `si/sino`, `mientras`, `para`
- 📊 **Análisis estadísticos:** Clase incorporada con 8 métodos estadísticos
- 🖥️ **Interfaz gráfica:** Editor con tema nocturno moderno
- 🧪 **Tests completos:** 9 casos de prueba representativos

## 🏗️ Estructura del Proyecto

```
Cñ/
├── 📁 src/
│   ├── 🔍 lexer.py        # Analizador léxico (tokenización)
│   ├── 🌳 parser.py       # Analizador sintáctico (AST)
│   ├── ⚡ evaluator.py    # Evaluador + clase Estadisticas
│   ├── 🖼️ gui.py          # Interfaz gráfica nocturna
│   ├── 🚪 main.py         # Punto de entrada
│   └── 📚 README.md       # Esta documentación
├── 🧪 tests/
│   ├── 📋 README_TESTS.md # Documentación de tests
│   └── 📄 *.txt           # 9 casos de prueba
├── 📊 ESTADISTICAS.md     # Documentación de análisis estadísticos
└── 🖼️ logo_UNAL.png       # Logo de la universidad
```

## 🛠️ Instalación

### Prerrequisitos
- 🐍 Python 3.11 o superior
- 📦 pip (administrador de paquetes)

### Pasos de instalación

1. **Clona o descarga el proyecto:**
   ```bash
   git clone <url-del-repositorio>
   cd Cñ
   ```

2. **Crea un entorno virtual (recomendado):**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install ply pillow
   ```

## 🚀 Uso

### Interfaz Gráfica (Recomendado)
```bash
cd src
python gui.py
```

### Línea de Comandos
```bash
cd src
python main.py
```

### 🎯 Funcionalidades Disponibles

#### 📝 **Editor de Código**
- Carga archivos `.txt` con código Cñ
- Resaltado de sintaxis visual
- Tema nocturno para programación cómoda

#### 🔍 **Análisis Léxico**
Reconoce y clasifica tokens:
- Tipos de datos: `entero`, `real`, `arreglo`
- Operadores: `+`, `-`, `*`, `/`, `%`, `==`, `!=`, `<`, `>`, `<=`, `>=`
- Estructuras: `si`, `sino`, `mientras`, `para`, `regresa`
- Delimitadores: `(`, `)`, `{`, `}`, `[`, `]`, `;`, `,`, `.`

#### 🌳 **Análisis Sintáctico**
- Verifica la estructura gramatical del código
- Construye el Árbol de Sintaxis Abstracta (AST)
- Reporta errores de sintaxis con mensajes claros

#### ⚡ **Evaluación**
- Ejecuta el código Cñ paso a paso
- Maneja variables, arrays y operaciones aritméticas
- Soporte para funciones y análisis estadísticos

## 📊 Análisis Estadísticos

La clase `Estadisticas` proporciona métodos para análisis de datos:

```cñ
entero main() {
    arreglo entero datos[5] = {10, 20, 30, 40, 50};
    real promedio = Estadisticas.promedio(datos);
    regresa promedio; // Resultado: 30.0
}
```

### 🧮 Métodos disponibles:
- `promedio()` - Media aritmética
- `mediana()` - Valor central
- `moda()` - Valor más frecuente  
- `desviacion_estandar()` - Dispersión de datos
- `minimo()` / `maximo()` - Valores extremos
- `rango()` - Diferencia max-min
- `suma()` - Total acumulado

## 🧪 Tests y Ejemplos

### Tests Disponibles:
1. **`test_for.txt`** - 🔁 Bucles básicos
2. **`test_array_max.txt`** - 📊 Búsqueda en arrays
3. **`test_array_sort.txt`** - 🔄 Ordenamiento burbuja
4. **`test_array_fibonacci.txt`** - 🔢 Secuencia Fibonacci
5. **`test_for_factorial.txt`** - ➗ Cálculo factorial
6. **`test_real_basico.txt`** - 🔢 Números decimales
7. **`test_mixto_entero_real.txt`** - 🔄 Tipos mixtos
8. **`test_division_entera.txt`** - ➗ División entera vs real
9. **`test_estadisticas_basico.txt`** - 📈 Análisis estadístico

### Ejemplo de código Cñ:

```cñ
entero main() {
    // Declaración de array con inicialización
    arreglo entero numeros[5] = {15, 8, 23, 4, 16};
    
    // Variables para resultados
    real promedio;
    entero maximo;
    
    // Análisis estadístico
    promedio = Estadisticas.promedio(numeros);
    maximo = Estadisticas.maximo(numeros);
    
    // Estructura de control
    si (promedio > 10) {
        regresa maximo;
    } sino {
        regresa 0;
    }
}
```

## 🎨 Interfaz Gráfica

### Características del Editor:
- 🌙 **Tema nocturno** moderno y elegante
- 📝 **Editor de código** con syntax highlighting visual
- 🔍 **Panel de análisis léxico** con tokens identificados
- ✅ **Estado sintáctico** (aceptado/rechazado)
- 📤 **Output** con resultados de ejecución
- 📁 **Carga de archivos** .txt integrada

### Paleta de Colores:
- 🖤 Fondo: `#1e1e2e` (azul oscuro)
- 📝 Texto: `#cdd6f4` (blanco suave)  
- 🔵 Botones: `#89b4fa` (azul vibrante)
- 🟢 Acentos: `#a6e3a1` (verde suave)
- 🟣 Títulos: `#cba6f7` (púrpura)

## 🤝 Contribución

¡Las contribuciones son bienvenidas! 

### Para contribuir:
1. 🍴 Haz fork del proyecto
2. 🌿 Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit tus cambios (`git commit -m 'Add: AmazingFeature'`)
4. 📤 Push a la rama (`git push origin feature/AmazingFeature`)
5. 🔄 Abre un Pull Request

## 📋 Tareas Futuras

- [ ] 🔧 Más funciones matemáticas
- [ ] 📝 Soporte para strings
- [ ] 🔍 Debugging paso a paso
- [ ] 📊 Más análisis estadísticos
- [ ] 🎨 Más temas de colores
- [ ] 📱 Versión web

## 🐛 Reporte de Errores

Si encuentras algún bug o tienes sugerencias:
1. 📝 Abre un issue en GitHub
2. 🔍 Describe el problema detalladamente  
3. 📎 Incluye código de ejemplo si es posible

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👥 Autores

- **Equipo de Desarrollo** - Proyecto académico Universidad Nacional de Colombia

---

⭐ **¡Si te gusta el proyecto, dale una estrella!** ⭐
