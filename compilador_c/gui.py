import tkinter as tk
from lexer import lexer
from parser import parser, symbol_table

#  Numeración de líneas
class LineNumbers(tk.Canvas):
    def __init__(self, text_widget, **kwargs):
        super().__init__(**kwargs)
        self.text_widget = text_widget
        self.text_widget.bind("<KeyRelease>", self.update)
        self.text_widget.bind("<MouseWheel>", self.update)
        self.update()

    def update(self, event=None):
        self.delete("all")
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, font=("Courier", 10))
            i = self.text_widget.index(f"{i}+1line")

#  Mostrar errores como comentarios
def log_error(message, lineno=None):
    if lineno:
        salida.insert(f"{lineno + 1}.0", f"// ⚠️ {message}\n", "error")
    else:
        salida.insert(tk.END, f"// ⚠️ {message}\n", "error")
    salida.tag_config("error", foreground="red")

# ▶ Mostrar salida de ejecución
def log_output(message):
    salida.insert(tk.END, message + "\n")
    salida.see(tk.END)

#  Redefinir errores léxicos y sintácticos
def t_error(t):
    msg = f"Error léxico: '{t.value[0]}' en línea {t.lineno}"
    log_error(msg, t.lineno)
    t.lexer.skip(1)

def p_error(p):
    lineno = p.lineno if p else 1
    msg = f"Error sintáctico en '{p.value}' línea {lineno}" if p else "Error sintáctico inesperado"
    log_error(msg, lineno)

#  Semántica + ejecución
runtime_memory = {}

def check_declaration(var, symbol_table, lineno):
    if var not in symbol_table:
        log_error(f"Error semántico: variable '{var}' no declarada", lineno)

def check_assignment(var, value_type, symbol_table, lineno):
    declared_type = symbol_table.get(var)
    if declared_type and declared_type != value_type:
        log_error(f"Error semántico: tipo incompatible en asignación a '{var}'", lineno)

def ejecutar_asignacion(var, expr):
    try:
        valor = eval(expr, {}, runtime_memory)
        runtime_memory[var] = valor
    except Exception:
        log_output(f"⚠️ Error al evaluar expresión: {expr}")

def ejecutar_printf(cadena, var=None):
    texto = cadena.strip('"')
    if var:
        valor = runtime_memory.get(var, f"[{var} no definido]")
        log_output(f"{texto} {valor}")
    else:
        log_output(texto)

#  Analizar y ejecutar
def analizar_codigo():
    symbol_table.clear()
    runtime_memory.clear()
    salida.delete("1.0", tk.END)
    codigo = entrada.get("1.0", tk.END)
    salida.insert("1.0", codigo)

    lexer.input(codigo)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)

    parser.parse(codigo)

    # Simulación básica de ejecución
    lineas = codigo.splitlines()
    for i, linea in enumerate(lineas):
        if "=" in linea and ";" in linea:
            partes = linea.replace(";", "").split("=")
            var = partes[0].strip()
            expr = partes[1].strip()
            ejecutar_asignacion(var, expr)
        elif "printf" in linea:
            contenido = linea[linea.find("(")+1:linea.find(")")]
            args = [x.strip() for x in contenido.split(",")]
            if len(args) == 2:
                ejecutar_printf(args[0], args[1])
            elif len(args) == 1:
                ejecutar_printf(args[0])

# Interfaz
ventana = tk.Tk()
ventana.title("Compilador C - Interfaz Gráfica")
ventana.geometry("900x700")

tk.Label(ventana, text="Código fuente (C):", font=("Arial", 12)).pack(anchor="w", padx=10, pady=(10, 0))
frame_editor = tk.Frame(ventana)
frame_editor.pack(padx=10)

entrada = tk.Text(frame_editor, width=100, height=20, font=("Courier", 10))
entrada.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

lineas = LineNumbers(entrada, width=30)
lineas.pack(side=tk.LEFT, fill=tk.Y)

tk.Button(ventana, text="Analizar y Ejecutar", command=analizar_codigo, bg="lightblue", font=("Arial", 11)).pack(pady=10)

tk.Label(ventana, text="Salida:", font=("Arial", 12)).pack(anchor="w", padx=10)
salida = tk.Text(ventana, width=100, height=15, font=("Courier", 10))
salida.pack(padx=10, pady=(0, 10))

ventana.mainloop()
