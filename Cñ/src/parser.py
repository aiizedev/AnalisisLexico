# filepath: /c_like_calc/c_like_calc/src/parser.py
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.position = 0
        self.symbol_table = {}  # Para tipos
        self.next_token()

    def next_token(self):
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
            self.position += 1
        else:
            self.current_token = None

    def parse(self):
        clases = []
        
        # Primero parsear las clases si existen
        while self.current_token is not None and self.current_token['type'] == 'CLASE':
            clases.append(self.definicion_clase())
        
        # Luego el programa debe iniciar con: entero main() { ... } o real main() { ... }
        if self.current_token['type'] in ('ENTERO', 'REAL'):
            tipo_main = self.current_token['type']
            self.next_token()
            if self.current_token['type'] != 'IDENTIFICADOR' or self.current_token['value'] != 'main':
                raise SyntaxError("Se esperaba 'main' después del tipo de dato")
            self.next_token()
            if self.current_token['type'] != 'PARI':
                raise SyntaxError("Se esperaba '(' después de 'main'")
            self.next_token()
            if self.current_token['type'] != 'PARD':
                raise SyntaxError("Se esperaba ')' después de '(' en la declaración de main")
            self.next_token()
            if self.current_token['type'] != 'LLAVEI':
                raise SyntaxError("Se esperaba '{' después de la declaración de main")
            bloque = self.bloque()
            return {'type': 'program', 'classes': clases, 'main': {'type': 'main_function', 'return_type': tipo_main, 'body': bloque}}
        else:
            raise SyntaxError("Se esperaba 'entero main()' o 'real main()' al inicio del programa")

    def bloque(self):
        if self.current_token['type'] != 'LLAVEI':
            raise SyntaxError("Se esperaba '{' para iniciar el bloque")
        self.next_token()
        sentencias = []
        while self.current_token is not None and self.current_token['type'] != 'LLAVED':
            sentencias.append(self.sentencia())
        if self.current_token is None or self.current_token['type'] != 'LLAVED':
            raise SyntaxError("Se esperaba '}' para cerrar el bloque")
        self.next_token()
        return sentencias

    def definicion_clase(self):
        # clase Estadisticas { ... }
        if self.current_token['type'] != 'CLASE':
            raise SyntaxError("Se esperaba 'clase'")
        self.next_token()
        
        if self.current_token['type'] != 'IDENTIFICADOR':
            raise SyntaxError("Se esperaba el nombre de la clase")
        nombre_clase = self.current_token['value']
        self.next_token()
        
        if self.current_token['type'] != 'LLAVEI':
            raise SyntaxError("Se esperaba '{' después del nombre de la clase")
        self.next_token()
        
        metodos = []
        while self.current_token is not None and self.current_token['type'] != 'LLAVED':
            metodos.append(self.definicion_metodo())
        
        if self.current_token is None or self.current_token['type'] != 'LLAVED':
            raise SyntaxError("Se esperaba '}' para cerrar la clase")
        self.next_token()
        
        return {'type': 'class_definition', 'name': nombre_clase, 'methods': metodos}

    def definicion_metodo(self):
        # real promedio(arreglo entero datos) { ... }
        tipo_retorno = self.current_token['type']
        if tipo_retorno not in ('ENTERO', 'REAL'):
            raise SyntaxError("Se esperaba tipo de retorno del método")
        self.next_token()
        
        if self.current_token['type'] != 'IDENTIFICADOR':
            raise SyntaxError("Se esperaba el nombre del método")
        nombre_metodo = self.current_token['value']
        self.next_token()
        
        if self.current_token['type'] != 'PARI':
            raise SyntaxError("Se esperaba '(' después del nombre del método")
        self.next_token()
        
        parametros = []
        while self.current_token is not None and self.current_token['type'] != 'PARD':
            parametros.append(self.parametro())
            if self.current_token['type'] == 'COMA':
                self.next_token()
            elif self.current_token['type'] != 'PARD':
                raise SyntaxError("Se esperaba ',' o ')' en la lista de parámetros")
        
        if self.current_token['type'] != 'PARD':
            raise SyntaxError("Se esperaba ')' para cerrar la lista de parámetros")
        self.next_token()
        
        if self.current_token['type'] != 'LLAVEI':
            raise SyntaxError("Se esperaba '{' para iniciar el cuerpo del método")
        
        cuerpo = self.bloque()
        
        return {'type': 'method_definition', 'return_type': tipo_retorno, 'name': nombre_metodo, 'parameters': parametros, 'body': cuerpo}

    def parametro(self):
        # arreglo entero datos  o  entero valor
        if self.current_token['type'] == 'ARREGLO':
            self.next_token()
            tipo_elemento = self.current_token['type']
            if tipo_elemento not in ('ENTERO', 'REAL'):
                raise SyntaxError("Se esperaba tipo después de 'arreglo'")
            self.next_token()
            if self.current_token['type'] != 'IDENTIFICADOR':
                raise SyntaxError("Se esperaba nombre del parámetro")
            nombre = self.current_token['value']
            self.next_token()
            return {'type': 'array_parameter', 'element_type': tipo_elemento, 'name': nombre}
        elif self.current_token['type'] in ('ENTERO', 'REAL'):
            tipo = self.current_token['type']
            self.next_token()
            if self.current_token['type'] != 'IDENTIFICADOR':
                raise SyntaxError("Se esperaba nombre del parámetro")
            nombre = self.current_token['value']
            self.next_token()
            return {'type': 'simple_parameter', 'var_type': tipo, 'name': nombre}
        else:
            raise SyntaxError("Se esperaba tipo de parámetro")

    def sentencia(self):
        tok_type = self.current_token['type']
        if tok_type in ('ENTERO', 'REAL'):
            return self.declaracion()
        elif tok_type == 'ARREGLO':
            return self.declaracion_arreglo()
        elif tok_type == 'NUEVO':
            return self.instanciacion_clase()
        elif tok_type == 'IDENTIFICADOR':
            # Verificar si es acceso a array, asignación normal, o llamada a método
            next_pos = self.position
            if next_pos < len(self.tokens):
                next_token_type = self.tokens[next_pos]['type']
                if next_token_type == 'CORCHETE_IZQ':
                    return self.asignacion_arreglo()
                elif next_token_type == 'PUNTO':
                    # Es una llamada a método
                    return self.llamada_metodo()
                else:
                    return self.asignacion()
            else:
                return self.asignacion()
        elif tok_type == 'REGRESA':
            return self.regresa()
        elif tok_type == 'SI':
            return self.si()
        elif tok_type == 'MIENTRAS':
            return self.mientras()
        elif tok_type == 'PARA':
            return self.para()
        elif tok_type == 'LLAVEI':
            return self.bloque()
        else:
            raise SyntaxError(f"Token inesperado: {self.current_token}")

    def declaracion(self):
        tipo = self.current_token['type']
        self.next_token()
        if self.current_token['type'] != 'IDENTIFICADOR':
            raise SyntaxError("Se esperaba un identificador después del tipo")
        nombre = self.current_token['value']
        self.symbol_table[nombre] = tipo
        self.next_token()
        
        # Verificar si hay asignación inicial
        valor = None
        if self.current_token['type'] == 'ASIGNA':
            self.next_token()
            valor = self.expresion()
        
        if self.current_token['type'] != 'PUNTOYCOMA':
            raise SyntaxError("Se esperaba ';' después de la declaración")
        self.next_token()
        return {'type': 'declaration', 'var_type': tipo, 'name': nombre, 'value': valor}

    def declaracion_sin_puntoycoma(self):
        tipo = self.current_token['type']
        self.next_token()
        if self.current_token['type'] != 'IDENTIFICADOR':
            raise SyntaxError("Se esperaba un identificador después del tipo")
        nombre = self.current_token['value']
        self.symbol_table[nombre] = tipo
        self.next_token()
        
        # Verificar si hay asignación inicial
        valor = None
        if self.current_token['type'] == 'ASIGNA':
            self.next_token()
            valor = self.expresion()
        
        return {'type': 'declaration', 'var_type': tipo, 'name': nombre, 'value': valor}

    def asignacion(self):
        identificador = self.current_token
        nombre = identificador['value']
        if nombre not in self.symbol_table:
            raise SyntaxError(f"Variable '{nombre}' no declarada")
        self.next_token()
        if self.current_token['type'] != 'ASIGNA':
            raise SyntaxError("Se esperaba '=' después del identificador")
        self.next_token()
        expr = self.expresion()
        if self.current_token['type'] != 'PUNTOYCOMA':
            raise SyntaxError("Se esperaba ';' después de la asignación")
        self.next_token()
        return {'type': 'assignment', 'identifier': identificador, 'expression': expr}

    def asignacion_sin_puntoycoma(self):
        identificador = self.current_token
        nombre = identificador['value']
        if nombre not in self.symbol_table:
            raise SyntaxError(f"Variable '{nombre}' no declarada")
        self.next_token()
        if self.current_token['type'] != 'ASIGNA':
            raise SyntaxError("Se esperaba '=' después del identificador")
        self.next_token()
        expr = self.expresion()
        return {'type': 'assignment', 'identifier': identificador, 'expression': expr}

    def regresa(self):
        self.next_token()
        expr = self.expresion()
        if self.current_token['type'] != 'PUNTOYCOMA':
            raise SyntaxError("Se esperaba ';' después de 'regresa'")
        self.next_token()
        return {'type': 'return', 'expression': expr}

    def si(self):
        self.next_token()
        if self.current_token['type'] != 'PARI':
            raise SyntaxError("Se esperaba '(' después de 'si'")
        self.next_token()
        condicion = self.expresion()
        if self.current_token['type'] != 'PARD':
            raise SyntaxError("Se esperaba ')' después de la condición")
        self.next_token()
        bloque_si = self.bloque()
        bloque_sino = None
        if self.current_token and self.current_token['type'] == 'SINO':
            self.next_token()
            bloque_sino = self.bloque()
        return {'type': 'if', 'condition': condicion, 'then': bloque_si, 'else': bloque_sino}

    def mientras(self):
        self.next_token()
        if self.current_token['type'] != 'PARI':
            raise SyntaxError("Se esperaba '(' después de 'mientras'")
        self.next_token()
        condicion = self.expresion()
        if self.current_token['type'] != 'PARD':
            raise SyntaxError("Se esperaba ')' después de la condición")
        self.next_token()
        bloque = self.bloque()
        return {'type': 'while', 'condition': condicion, 'block': bloque}

    def para(self):
        self.next_token()
        if self.current_token['type'] != 'PARI':
            raise SyntaxError("Se esperaba '(' después de 'para'")
        self.next_token()
        
        # Inicialización (puede ser declaración o asignación)
        inicializacion = None
        if self.current_token['type'] in ('ENTERO', 'REAL'):
            inicializacion = self.declaracion_sin_puntoycoma()
        elif self.current_token['type'] == 'IDENTIFICADOR':
            inicializacion = self.asignacion_sin_puntoycoma()
        
        if self.current_token['type'] != 'PUNTOYCOMA':
            raise SyntaxError("Se esperaba ';' después de la inicialización del for")
        self.next_token()
        
        # Condición
        condicion = self.expresion()
        if self.current_token['type'] != 'PUNTOYCOMA':
            raise SyntaxError("Se esperaba ';' después de la condición del for")
        self.next_token()
        
        # Incremento
        incremento = None
        if self.current_token['type'] == 'IDENTIFICADOR':
            incremento = self.asignacion_sin_puntoycoma()
        
        if self.current_token['type'] != 'PARD':
            raise SyntaxError("Se esperaba ')' después del incremento del for")
        self.next_token()
        
        bloque = self.bloque()
        return {
            'type': 'for', 
            'init': inicializacion, 
            'condition': condicion, 
            'increment': incremento, 
            'block': bloque
        }

    def declaracion_arreglo(self):
        # arreglo entero nombre[tamaño];
        # arreglo entero nombre[tamaño] = {valores};
        self.next_token()  # consumir 'arreglo'
        
        if self.current_token['type'] not in ('ENTERO', 'REAL'):
            raise SyntaxError("Se esperaba tipo de dato después de 'arreglo'")
        
        tipo_elemento = self.current_token['type']
        self.next_token()
        
        if self.current_token['type'] != 'IDENTIFICADOR':
            raise SyntaxError("Se esperaba nombre del arreglo")
        
        nombre = self.current_token['value']
        self.next_token()
        
        if self.current_token['type'] != 'CORCHETE_IZQ':
            raise SyntaxError("Se esperaba '[' para el tamaño del arreglo")
        self.next_token()
        
        tamaño = self.expresion()
        
        if self.current_token['type'] != 'CORCHETE_DER':
            raise SyntaxError("Se esperaba ']' después del tamaño del arreglo")
        self.next_token()
        
        # Verificar si hay inicialización
        valores = None
        if self.current_token['type'] == 'ASIGNA':
            self.next_token()
            if self.current_token['type'] != 'LLAVEI':
                raise SyntaxError("Se esperaba '{' para inicializar el arreglo")
            self.next_token()
            
            valores = []
            if self.current_token['type'] != 'LLAVED':  # Arreglo no vacío
                valores.append(self.expresion())
                while self.current_token['type'] == 'COMA':
                    self.next_token()
                    valores.append(self.expresion())
            
            if self.current_token['type'] != 'LLAVED':
                raise SyntaxError("Se esperaba '}' para cerrar la inicialización")
            self.next_token()
        
        if self.current_token['type'] != 'PUNTOYCOMA':
            raise SyntaxError("Se esperaba ';' después de la declaración del arreglo")
        self.next_token()
        
        self.symbol_table[nombre] = f'array_{tipo_elemento}'
        return {
            'type': 'array_declaration',
            'element_type': tipo_elemento,
            'name': nombre,
            'size': tamaño,
            'values': valores
        }

    def asignacion_arreglo(self):
        # nombre[indice] = valor;
        identificador = self.current_token
        nombre = identificador['value']
        if nombre not in self.symbol_table:
            raise SyntaxError(f"Arreglo '{nombre}' no declarado")
        
        self.next_token()  # consumir identificador
        
        if self.current_token['type'] != 'CORCHETE_IZQ':
            raise SyntaxError("Se esperaba '[' para acceso al arreglo")
        self.next_token()
        
        indice = self.expresion()
        
        if self.current_token['type'] != 'CORCHETE_DER':
            raise SyntaxError("Se esperaba ']' después del índice")
        self.next_token()
        
        if self.current_token['type'] != 'ASIGNA':
            raise SyntaxError("Se esperaba '=' para asignación al arreglo")
        self.next_token()
        
        valor = self.expresion()
        
        if self.current_token['type'] != 'PUNTOYCOMA':
            raise SyntaxError("Se esperaba ';' después de la asignación del arreglo")
        self.next_token()
        
        return {
            'type': 'array_assignment',
            'identifier': identificador,
            'index': indice,
            'value': valor
        }

    def expresion(self):
        left = self.expresion_arit()
        while self.current_token and self.current_token['type'] in (
            'IGUAL', 'DIF', 'MENOR', 'MAYOR', 'MENORI', 'MAYORI'
        ):
            op = self.current_token
            self.next_token()
            right = self.expresion_arit()
            left = {'type': 'binary_op', 'op': op, 'left': left, 'right': right}
        return left

    def expresion_arit(self):
        left = self.termino()
        while self.current_token and self.current_token['type'] in ('MAS', 'MENOS'):
            op = self.current_token
            self.next_token()
            right = self.termino()
            left = {'type': 'binary_op', 'op': op, 'left': left, 'right': right}
        return left

    def termino(self):
        left = self.factor()
        while self.current_token and self.current_token['type'] in ('POR', 'DIVIDIDO', 'MOD'):
            op = self.current_token
            self.next_token()
            right = self.factor()
            left = {'type': 'binary_op', 'op': op, 'left': left, 'right': right}
        return left

    def factor(self):
        tok = self.current_token
        if tok['type'] == 'NUMERO':
            self.next_token()
            return tok
        elif tok['type'] == 'IDENTIFICADOR':
            identificador = tok
            self.next_token()
            
            # Verificar si es acceso a método estático (Clase.metodo)
            if self.current_token and self.current_token['type'] == 'PUNTO':
                self.next_token()
                if self.current_token['type'] != 'IDENTIFICADOR':
                    raise SyntaxError("Se esperaba nombre del método después de '.'")
                
                nombre_metodo = self.current_token['value']
                self.next_token()
                
                if self.current_token['type'] != 'PARI':
                    raise SyntaxError("Se esperaba '(' para los argumentos del método")
                self.next_token()
                
                argumentos = []
                while self.current_token is not None and self.current_token['type'] != 'PARD':
                    argumentos.append(self.expresion())
                    if self.current_token['type'] == 'COMA':
                        self.next_token()
                    elif self.current_token['type'] != 'PARD':
                        raise SyntaxError("Se esperaba ',' o ')' en los argumentos del método")
                
                if self.current_token['type'] != 'PARD':
                    raise SyntaxError("Se esperaba ')' para cerrar los argumentos")
                self.next_token()
                
                return {
                    'type': 'method_call_expression',
                    'object': identificador['value'],
                    'method': nombre_metodo,
                    'arguments': argumentos
                }
            # Verificar si es acceso a arreglo
            elif self.current_token and self.current_token['type'] == 'CORCHETE_IZQ':
                self.next_token()
                indice = self.expresion()
                if self.current_token['type'] != 'CORCHETE_DER':
                    raise SyntaxError("Se esperaba ']' después del índice")
                self.next_token()
                return {
                    'type': 'array_access',
                    'identifier': identificador,
                    'index': indice
                }
            else:
                return identificador
        elif tok['type'] == 'LONGITUD':
            self.next_token()
            if self.current_token['type'] != 'PARI':
                raise SyntaxError("Se esperaba '(' después de 'longitud'")
            self.next_token()
            
            if self.current_token['type'] != 'IDENTIFICADOR':
                raise SyntaxError("Se esperaba nombre del arreglo en longitud()")
            
            arreglo = self.current_token
            self.next_token()
            
            if self.current_token['type'] != 'PARD':
                raise SyntaxError("Se esperaba ')' después del nombre del arreglo")
            self.next_token()
            
            return {
                'type': 'array_length',
                'array': arreglo
            }
        elif tok['type'] == 'PARI':
            self.next_token()
            expr = self.expresion()
            if self.current_token['type'] != 'PARD':
                raise SyntaxError("Se esperaba ')'")
            self.next_token()
            return expr
        else:
            raise SyntaxError(f"Token inesperado en factor: {tok}")

    def instanciacion_clase(self):
        # nuevo Estadisticas() asignado a una variable
        # Esto debe ser parte de una declaración: Estadisticas stats = nuevo Estadisticas();
        if self.current_token['type'] != 'NUEVO':
            raise SyntaxError("Se esperaba 'nuevo'")
        self.next_token()
        
        if self.current_token['type'] != 'IDENTIFICADOR':
            raise SyntaxError("Se esperaba nombre de la clase después de 'nuevo'")
        nombre_clase = self.current_token['value']
        self.next_token()
        
        if self.current_token['type'] != 'PARI':
            raise SyntaxError("Se esperaba '(' después del nombre de la clase")
        self.next_token()
        
        if self.current_token['type'] != 'PARD':
            raise SyntaxError("Se esperaba ')' para cerrar la instanciación")
        self.next_token()
        
        if self.current_token['type'] != 'PUNTOYCOMA':
            raise SyntaxError("Se esperaba ';' después de la instanciación")
        self.next_token()
        
        return {'type': 'class_instantiation', 'class_name': nombre_clase}

    def llamada_metodo(self):
        # objeto.metodo(parametros);
        if self.current_token['type'] != 'IDENTIFICADOR':
            raise SyntaxError("Se esperaba identificador del objeto")
        nombre_objeto = self.current_token['value']
        self.next_token()
        
        if self.current_token['type'] != 'PUNTO':
            raise SyntaxError("Se esperaba '.' después del nombre del objeto")
        self.next_token()
        
        if self.current_token['type'] != 'IDENTIFICADOR':
            raise SyntaxError("Se esperaba nombre del método")
        nombre_metodo = self.current_token['value']
        self.next_token()
        
        if self.current_token['type'] != 'PARI':
            raise SyntaxError("Se esperaba '(' para los argumentos del método")
        self.next_token()
        
        argumentos = []
        while self.current_token is not None and self.current_token['type'] != 'PARD':
            argumentos.append(self.expresion())
            if self.current_token['type'] == 'COMA':
                self.next_token()
            elif self.current_token['type'] != 'PARD':
                raise SyntaxError("Se esperaba ',' o ')' en los argumentos del método")
        
        if self.current_token['type'] != 'PARD':
            raise SyntaxError("Se esperaba ')' para cerrar los argumentos")
        self.next_token()
        
        if self.current_token['type'] != 'PUNTOYCOMA':
            raise SyntaxError("Se esperaba ';' después de la llamada al método")
        self.next_token()
        
        return {'type': 'method_call', 'object': nombre_objeto, 'method': nombre_metodo, 'arguments': argumentos}