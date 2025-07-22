# filepath: /c_like_calc/c_like_calc/src/main.py
from lexer import lexer
from parser import Parser
from evaluator import Evaluator

def tokenize(code):
    lexer.input(code)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append({'type': tok.type, 'value': tok.value})
    return tokens

def main():
    print("Introduce tu código C-like (finaliza con una línea vacía):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    code = "\n".join(lines)
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    evaluator = Evaluator()
    result = evaluator.eval_program(ast)
    print("Resultado:", result)

if __name__ == "__main__":
    main()