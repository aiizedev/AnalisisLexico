# evaluator.py
import math

class Estadisticas:
    """Clase incorporada para análisis estadísticos"""
    
    def promedio(self, datos):
        if not datos:
            return 0.0
        return sum(datos) / len(datos)
    
    def mediana(self, datos):
        if not datos:
            return 0.0
        datos_ordenados = sorted(datos)
        n = len(datos_ordenados)
        if n % 2 == 0:
            return (datos_ordenados[n//2-1] + datos_ordenados[n//2]) / 2.0
        return float(datos_ordenados[n//2])
    
    def moda(self, datos):
        if not datos:
            return 0.0
        contador = {}
        for valor in datos:
            contador[valor] = contador.get(valor, 0) + 1
        moda_valor = max(contador, key=contador.get)
        return float(moda_valor)
    
    def desviacion_estandar(self, datos):
        if len(datos) <= 1:
            return 0.0
        prom = self.promedio(datos)
        varianza = sum((x - prom) ** 2 for x in datos) / (len(datos) - 1)
        return math.sqrt(varianza)
    
    def minimo(self, datos):
        if not datos:
            return 0.0
        return float(min(datos))
    
    def maximo(self, datos):
        if not datos:
            return 0.0
        return float(max(datos))
    
    def rango(self, datos):
        if not datos:
            return 0.0
        return self.maximo(datos) - self.minimo(datos)
    
    def suma(self, datos):
        return float(sum(datos))

class Evaluator:
    def __init__(self):
        self.env = {}
        self.arrays = {}  # Almacenar arrays separadamente
        self.classes = {}  # Definiciones de clases
        self.objects = {}  # Instancias de objetos

    def eval(self, node):
        node_type = node['type']
        
        # Manejar arrays
        if node_type == 'array_declaration':
            name = node['name']
            element_type = node.get('element_type', 'ENTERO')
            size_val = self.eval(node['size'])
            
            if not isinstance(size_val, int) or size_val <= 0:
                raise Exception(f"El tamaño del arreglo debe ser un entero positivo")
            
            # Valor por defecto según el tipo
            default_value = 0.0 if element_type == 'REAL' else 0
            
            # Inicializar el array
            if node['values']:
                # Con valores iniciales
                valores = [self.eval(val) for val in node['values']]
                if len(valores) > size_val:
                    raise Exception(f"Demasiados valores para inicializar el arreglo de tamaño {size_val}")
                # Rellenar con valores por defecto si faltan valores
                while len(valores) < size_val:
                    valores.append(default_value)
                self.arrays[name] = valores
            else:
                # Sin valores iniciales, rellenar con valores por defecto
                self.arrays[name] = [default_value] * size_val
            
            return None
            
        elif node_type == 'array_assignment':
            name = node['identifier']['value']
            if name not in self.arrays:
                raise Exception(f"Arreglo '{name}' no declarado")
            
            index = self.eval(node['index'])
            value = self.eval(node['value'])
            
            if not isinstance(index, int):
                raise Exception(f"El índice debe ser un entero")
            
            if index < 0 or index >= len(self.arrays[name]):
                raise Exception(f"Índice {index} fuera de rango para el arreglo '{name}'")
            
            self.arrays[name][index] = value
            return None
            
        elif node_type == 'array_access':
            name = node['identifier']['value']
            if name not in self.arrays:
                raise Exception(f"Arreglo '{name}' no declarado")
            
            index = self.eval(node['index'])
            
            if not isinstance(index, int):
                raise Exception(f"El índice debe ser un entero")
            
            if index < 0 or index >= len(self.arrays[name]):
                raise Exception(f"Índice {index} fuera de rango para el arreglo '{name}'")
            
            return self.arrays[name][index]
            
        elif node_type == 'array_length':
            name = node['array']['value']
            if name not in self.arrays:
                raise Exception(f"Arreglo '{name}' no declarado")
            
            return len(self.arrays[name])
            
        # Manejar otros tipos de nodos
        elif node_type == 'return':
            return {'type': 'return', 'value': self.eval(node['expression'])}
            
        elif node_type == 'assignment':
            name = node['identifier']['value']
            value = self.eval(node['expression'])
            self.env[name] = value
            return None
            
        elif node_type == 'class_instantiation':
            # nuevo Estadisticas()
            class_name = node['class_name']
            if class_name == 'Estadisticas':
                return Estadisticas()
            else:
                raise Exception(f"Clase '{class_name}' no encontrada")
        
        elif node_type == 'method_call':
            # objeto.metodo(argumentos)
            object_name = node['object']
            method_name = node['method']
            arguments = [self.eval(arg) for arg in node['arguments']]
            
            # Si es la clase Estadisticas incorporada
            if object_name == 'Estadisticas':
                stats = self.objects['Estadisticas']
                if hasattr(stats, method_name):
                    method = getattr(stats, method_name)
                    return method(*arguments)
                else:
                    raise Exception(f"Método '{method_name}' no encontrado en Estadisticas")
            else:
                raise Exception(f"Objeto '{object_name}' no encontrado")
                
        elif node_type == 'method_call_expression':
            # Similar a method_call pero dentro de expresiones
            object_name = node['object']
            method_name = node['method']
            arguments = [self.eval(arg) for arg in node['arguments']]
            
            # Si es la clase Estadisticas incorporada
            if object_name == 'Estadisticas':
                stats = self.objects['Estadisticas']
                if hasattr(stats, method_name):
                    method = getattr(stats, method_name)
                    return method(*arguments)
                else:
                    raise Exception(f"Método '{method_name}' no encontrado en Estadisticas")
            else:
                raise Exception(f"Objeto '{object_name}' no encontrado")
            
        elif node_type == 'if':
            cond = self.eval(node['condition'])
            if cond:
                for stmt in node['then']:
                    result = self.eval(stmt)
                    if isinstance(result, dict) and result.get('type') == 'return':
                        return result
            elif node['else']:
                for stmt in node['else']:
                    result = self.eval(stmt)
                    if isinstance(result, dict) and result.get('type') == 'return':
                        return result
            return None
            
        elif node_type == 'while':
            while self.eval(node['condition']):
                for stmt in node['block']:
                    result = self.eval(stmt)
                    if isinstance(result, dict) and result.get('type') == 'return':
                        return result
            return None
            
        elif node_type == 'for':
            # Ejecutar inicialización
            if node['init']:
                self.eval(node['init'])
            
            # Ejecutar el bucle
            while self.eval(node['condition']):
                # Ejecutar el bloque
                for stmt in node['block']:
                    result = self.eval(stmt)
                    if isinstance(result, dict) and result.get('type') == 'return':
                        return result
                
                # Ejecutar incremento
                if node['increment']:
                    self.eval(node['increment'])
            return None
            
        elif node_type == 'binary_op':
            left = self.eval(node['left'])
            right = self.eval(node['right'])
            op = node['op']['type']
            if op == 'MAS': return left + right
            if op == 'MENOS': return left - right
            if op == 'POR': return left * right
            if op == 'DIVIDIDO': 
                if isinstance(left, int) and isinstance(right, int):
                    return left // right  # División entera
                else:
                    return left / right   # División decimal
            if op == 'MOD': return left % right
            if op == 'IGUAL': return left == right
            if op == 'DIF': return left != right
            if op == 'MENOR': return left < right
            if op == 'MAYOR': return left > right
            if op == 'MENORI': return left <= right
            if op == 'MAYORI': return left >= right
            
        elif node_type in ('NUMBER', 'VALUE', 'NUMERO'):
            return node['value']
            
        elif node_type == 'IDENTIFICADOR':
            name = node['value']
            # Primero buscar en arrays, luego en variables normales
            if name in self.arrays:
                return self.arrays[name]
            elif name in self.env:
                return self.env[name]
            else:
                return 0
            
        elif node_type == 'main_function':
            return self.eval_program(node['body'])
            
        elif node_type == 'declaration':
            name = node['name']
            var_type = node.get('var_type', 'ENTERO')
            # Si hay un valor inicial, usarlo; si no, inicializar según el tipo
            if 'value' in node and node['value'] is not None:
                self.env[name] = self.eval(node['value'])
            else:
                # Inicialización por defecto según el tipo
                if var_type == 'REAL':
                    self.env[name] = 0.0
                else:
                    self.env[name] = 0
            return None
            
        else:
            raise Exception(f"Unknown node type: {node_type}")

    def eval_program(self, program):
        # Manejar la nueva estructura con clases
        if isinstance(program, dict):
            if program.get('type') == 'program':
                # Registrar las clases
                for class_def in program.get('classes', []):
                    self.classes[class_def['name']] = class_def
                
                # Agregar la clase Estadisticas incorporada
                self.objects['Estadisticas'] = Estadisticas()
                
                # Ejecutar el main
                main_program = program['main']['body']
            elif program.get('type') == 'main_function':
                main_program = program['body']
            else:
                main_program = [program]
        else:
            main_program = program
            
        for stmt in main_program:
            result = self.eval(stmt)
            if isinstance(result, dict) and result.get('type') == 'return':
                return result['value']
        return None
