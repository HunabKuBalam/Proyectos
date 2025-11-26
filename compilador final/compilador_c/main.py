from lexer import lexer
from parser import parser

with open("entrada.c", "r") as f:
    data = f.read()

print(" Tokens encontrados:")
lexer.input(data)
for tok in lexer:
    print(f"{tok.type}({tok.value}) en línea {tok.lineno}")

print("\n Análisis sintáctico:")
parser.parse(data)
