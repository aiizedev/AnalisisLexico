import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from PIL import Image, ImageTk
from lexer import lexer
from parser import Parser
from evaluator import Evaluator
import os

PASTEL_VERDE = "#b7e4c7"
CUADRO_BORDE = 2

# Paleta de colores nocturna
DARK_BG = "#1e1e2e"          # Fondo principal oscuro
DARK_SURFACE = "#313244"     # Superficie de componentes
DARK_TEXT = "#cdd6f4"        # Texto principal claro
ACCENT_BLUE = "#89b4fa"      # Azul de acento
ACCENT_GREEN = "#a6e3a1"     # Verde de acento
ACCENT_PURPLE = "#cba6f7"    # Púrpura de acento
DARK_BORDER = "#45475a"      # Color de bordes

def tokenize(code):
    lexer.input(code)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append({'type': tok.type, 'value': tok.value})
    return tokens

def load_file():
    """Carga un archivo .txt y lo muestra en el área de código"""
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                code_input.delete("1.0", tk.END)
                code_input.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")

def analyze():
    code = code_input.get("1.0", tk.END)
    tokens = tokenize(code)
    lex_output.delete("1.0", tk.END)

    simbolos = {
        'ENTERO': '<Tipo de dato> entero',
        'REAL': '<Tipo de dato> real',
        'IDENTIFICADOR': '<Identificador>',
        'NUMERO': '<Número>',
        'MAS': '<Operador suma> +',
        'MENOS': '<Operador resta> -',
        'POR': '<Operador multiplicación> *',
        'DIVIDIDO': '<Operador división> /',
        'MOD': '<Operador módulo> %',
        'ASIGNA': '<Asignación> =',
        'PUNTOYCOMA': '<Fin de instrucción> ;',
        'PARI': '<Paréntesis de apertura> (',
        'PARD': '<Paréntesis de cierre> )',
        'LLAVEI': '<Llave de apertura> {',
        'LLAVED': '<Llave de cierre> }',
        'CORCHETE_IZQ': '<Corchete de apertura> [',
        'CORCHETE_DER': '<Corchete de cierre> ]',
        'COMA': '<Separador> ,',
        'PUNTO': '<Acceso miembro> .',
        'SI': '<Reservada si>',
        'SINO': '<Reservada sino>',
        'MIENTRAS': '<Reservada mientras>',
        'PARA': '<Reservada para>',
        'ARREGLO': '<Reservada arreglo>',
        'LONGITUD': '<Función longitud>',
        'REGRESA': '<Reservada regresa>',
        'CLASE': '<Reservada clase>',
        'NUEVO': '<Reservada nuevo>',
        'IGUAL': '<Operador igual> ==',
        'DIF': '<Operador diferente> !=',
        'MENOR': '<Operador menor> <',
        'MAYOR': '<Operador mayor> >',
        'MENORI': '<Operador menor o igual> <=',
        'MAYORI': '<Operador mayor o igual> >='
    }

    lines = code.split('\n')
    idx = 0
    for line_num, line in enumerate(lines, 1):
        line_tokens = []
        while idx < len(tokens):
            token_str = str(tokens[idx]['value'])
            # Si el token pertenece a la línea actual
            if token_str in line or tokens[idx]['type'] == 'NUMERO':
                tipo = tokens[idx]['type']
                valor = tokens[idx]['value']
                # Si es main, lo mostramos como reservada main
                if tipo == 'IDENTIFICADOR' and valor == 'main':
                    descripcion = '<Reservada main>'
                else:
                    descripcion = simbolos.get(tipo, f'<{tipo}>')
                line_tokens.append((descripcion, valor))
                idx += 1
            else:
                break
        if line.strip():
            lex_output.insert(tk.END, f"LINEA {line_num}\tSIMBOLO\n")
            for desc, val in line_tokens:
                lex_output.insert(tk.END, f"  {desc}\t{val}\n")
    if not lex_output.get("1.0", tk.END).strip():
        lex_output.insert(tk.END, "No se encontraron tokens.\n")

    try:
        parser = Parser(tokens)
        ast = parser.parse()
        syn_output.delete("1.0", tk.END)
        syn_output.insert(tk.END, "Aceptado")
        evaluator = Evaluator()
        result = evaluator.eval_program(ast)
        output_output.delete("1.0", tk.END)
        output_output.insert(tk.END, f"{result}")
    except Exception as e:
        syn_output.delete("1.0", tk.END)
        syn_output.insert(tk.END, f"Rechazado: {e}")
        output_output.delete("1.0", tk.END)
        output_output.insert(tk.END, "Error")

root = tk.Tk()
root.title("Cñ - Editor Nocturno")
root.configure(bg=DARK_BG)

# --- Encabezado con imagen y título ---
header_frame = tk.Frame(root, bg=DARK_BG)
header_frame.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)

img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logo_UNAL.png"))
try:
    img = Image.open(img_path)
    img = img.resize((120, 50), Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(img)
    img_label = tk.Label(header_frame, image=logo, bg=DARK_BG)
    img_label.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="w")
except Exception as e:
    print("Error al cargar la imagen:", e)
    img_label = tk.Label(header_frame, text="[Logo no encontrado]", bg=DARK_BG, fg=DARK_TEXT, font=("Montserrat", 12, "bold"))
    img_label.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="w")

title_label = tk.Label(header_frame, text="Cñ", font=("Montserrat", 22, "bold"), bg=DARK_BG, fg=ACCENT_PURPLE)
title_label.grid(row=0, column=1, pady=0, sticky="ns")  # Centrado vertical respecto a la imagen

header_frame.grid_columnconfigure(0, weight=0)
header_frame.grid_columnconfigure(1, weight=1)

# --- Recuadros principales ---
frame_font = ("Montserrat", 12, "bold")
label_args = {"bg": DARK_SURFACE, "fg": DARK_TEXT, "bd": CUADRO_BORDE, "font": frame_font, "labelanchor": "n"}

frame_input = tk.LabelFrame(root, text="Lenguaje", **label_args)
frame_lex = tk.LabelFrame(root, text="Análisis Léxico", **label_args)
frame_syn = tk.LabelFrame(root, text="Análisis Sintáctico", **label_args)
frame_output = tk.LabelFrame(root, text="Output", **label_args)

frame_input.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
frame_lex.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
frame_syn.grid(row=2, column=0, padx=10, pady=(2, 20), sticky="nsew")    
frame_output.grid(row=2, column=1, padx=10, pady=(2, 20), sticky="nsew") 

root.grid_rowconfigure(1, weight=3)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

code_input = scrolledtext.ScrolledText(frame_input, width=40, height=10, font=("Consolas", 11), 
                                     bg=DARK_BG, fg=DARK_TEXT, insertbackground=ACCENT_BLUE, 
                                     selectbackground=ACCENT_PURPLE, selectforeground=DARK_BG)
code_input.pack(fill="both", expand=True)

# Frame para los botones
button_frame = tk.Frame(frame_input, bg=DARK_SURFACE)
button_frame.pack(fill="x", pady=5)

tk.Button(button_frame, text="Cargar Archivo", command=load_file, bg=ACCENT_BLUE, fg=DARK_BG, 
          font=("Montserrat", 10, "bold"), activebackground=ACCENT_GREEN, activeforeground=DARK_BG,
          relief="flat", bd=0, padx=10, pady=5).pack(side="left", fill="x", expand=True, padx=(0, 2))
tk.Button(button_frame, text="Analizar", command=analyze, bg=ACCENT_GREEN, fg=DARK_BG, 
          font=("Montserrat", 10, "bold"), activebackground=ACCENT_BLUE, activeforeground=DARK_BG,
          relief="flat", bd=0, padx=10, pady=5).pack(side="right", fill="x", expand=True, padx=(2, 0))

lex_output = scrolledtext.ScrolledText(frame_lex, width=40, height=10, font=("Consolas", 11),
                                     bg=DARK_BG, fg=DARK_TEXT, insertbackground=ACCENT_BLUE,
                                     selectbackground=ACCENT_PURPLE, selectforeground=DARK_BG)
lex_output.pack(fill="both", expand=True)

syn_output = scrolledtext.ScrolledText(frame_syn, width=40, height=3, font=("Consolas", 11),
                                     bg=DARK_BG, fg=DARK_TEXT, insertbackground=ACCENT_BLUE,
                                     selectbackground=ACCENT_PURPLE, selectforeground=DARK_BG)
syn_output.pack(fill="both", expand=True)

output_output = scrolledtext.ScrolledText(frame_output, width=40, height=3, font=("Consolas", 11),
                                        bg=DARK_BG, fg=DARK_TEXT, insertbackground=ACCENT_BLUE,
                                        selectbackground=ACCENT_PURPLE, selectforeground=DARK_BG)
output_output.pack(fill="both", expand=True)

root.mainloop()