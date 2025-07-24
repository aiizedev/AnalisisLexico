# lexer.py
import ply.lex as lex

# List of token names
tokens = (
    'ENTERO', 'REAL', 'IDENTIFICADOR',
    'NUMERO',
    'MAS', 'MENOS', 'POR', 'DIVIDIDO', 'MOD',
    'ASIGNA', 'PUNTOYCOMA',
    'PARI', 'PARD', 'LLAVEI', 'LLAVED',
    'CORCHETE_IZQ', 'CORCHETE_DER',
    'SI', 'SINO', 'MIENTRAS', 'PARA', 'REGRESA',
    'ARREGLO', 'LONGITUD', 'COMA',
    'IGUAL', 'DIF', 'MENOR', 'MAYOR', 'MENORI', 'MAYORI',
    'CLASE', 'NUEVO', 'PUNTO'
)

# Regular expression rules for simple tokens
t_MAS      = r'\+'
t_MENOS    = r'-'
t_POR      = r'\*'
t_DIVIDIDO = r'/'
t_MOD      = r'%'
t_ASIGNA   = r'='
t_PUNTOYCOMA = r';'
t_PARI     = r'\('
t_PARD     = r'\)'
t_LLAVEI   = r'\{'
t_LLAVED   = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_COMA     = r','
t_PUNTO    = r'\.'
t_IGUAL    = r'=='
t_DIF      = r'!='
t_MENORI   = r'<='
t_MAYORI   = r'>='
t_MENOR    = r'<'
t_MAYOR    = r'>'

# Keywords
reserved = {
    'entero': 'ENTERO',
    'real': 'REAL',
    'si': 'SI',
    'sino': 'SINO',
    'mientras': 'MIENTRAS',
    'para': 'PARA',
    'arreglo': 'ARREGLO',
    'longitud': 'LONGITUD',
    'regresa': 'REGRESA',
    'clase': 'CLASE',
    'nuevo': 'NUEVO'
}

# Token for identifiers
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFICADOR')  # Check for keywords
    return t

# Token for numbers
def t_NUMERO(t):
    r'-?\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Token for float literals with special handling
def t_FLOTANTE(t):
    r'-?\d+\.\d+'
    t.type = 'NUMERO'
    t.value = float(t.value)
    return t

# Ignored characters
t_ignore = ' \t\r'

# Newline handling
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()