import tkinter as tk
from tkinter import ttk
from lexer import lexer, errors_lexicos
from parser import parser, symbol_table, Node, errors_sintacticos, automata_transitions
from semantic import errors_semanticos
from automata_gui import draw_automata_window   # importamos la ventana del autómata

#  Numeración de líneas
class LineNumbers(tk.Canvas):
    def __init__(self, text_widget, **kwargs):
        super().__init__(**kwargs)
        self.text_widget = text_widget
        for seq in ("<KeyRelease>", "<MouseWheel>", "<Button-1>", "<Configure>"):
            self.text_widget.bind(seq, self.update)
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

#  Insertar errores como comentarios rojos
def log_error(message, lineno=None):
    salida.tag_config("error", foreground="red")
    if lineno:
        salida.insert(f"{lineno + 1}.0", f"// ⚠️ {message}\n", "error")
    else:
        salida.insert(tk.END, f"// ⚠️ {message}\n", "error")

# Analizar y mostrar tokens, errores y abrir autómata
def analizar():
    # Limpiar acumuladores y UI
    symbol_table.clear()
    errors_lexicos.clear()
    errors_sintacticos.clear()
    errors_semanticos.clear()
    automata_transitions.clear()

    salida.delete("1.0", tk.END)
    panel_tokens.delete("1.0", tk.END)

    codigo = entrada.get("1.0", tk.END)
    salida.insert("1.0", codigo)

    # Tokens
    lexer.input(codigo)
    panel_tokens.insert(tk.END, "--- TOKENS ---\n")
    while True:
        tok = lexer.token()
        if not tok:
            break
        panel_tokens.insert(tk.END, f"{tok.type}({tok.value}) en línea {tok.lineno}\n")

    # Errores léxicos
    for msg, ln in errors_lexicos:
        log_error(msg, ln)

    # Parse
    root = parser.parse(codigo)

    # Errores sintácticos y semánticos
    for msg, ln in errors_sintacticos:
        log_error(msg, ln)
    for msg, ln in errors_semanticos:
        log_error(msg, ln)

    # Abrir ventana aparte con el autómata
    if automata_transitions:
        draw_automata_window(automata_transitions)
        panel_tokens.insert(tk.END, "\n--- Autómata del proceso generado ---\nSe abrió en una ventana aparte.\n")
    else:
        panel_tokens.insert(tk.END, "\nNo se generaron transiciones para el autómata.\n")

#  Interfaz principal
ventana = tk.Tk()
ventana.title("Compilador C - Tokens y errores")
ventana.geometry("1200x800")

tk.Label(ventana, text="Código fuente (C):", font=("Arial", 12)).pack(anchor="w", padx=10, pady=(10, 0))
frame_editor = tk.Frame(ventana)
frame_editor.pack(padx=10, fill=tk.BOTH)

entrada = tk.Text(frame_editor, width=110, height=20, font=("Courier", 10))
entrada.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

lineas = LineNumbers(entrada, width=40, bg="#f0f0f0")
lineas.pack(side=tk.LEFT, fill=tk.Y)

ttk.Button(ventana, text="Analizar", command=analizar).pack(pady=10)

# Notebook con pestañas
notebook = ttk.Notebook(ventana)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

frame_salida = tk.Frame(notebook)
frame_tokens = tk.Frame(notebook)

notebook.add(frame_salida, text="Salida (errores)")
notebook.add(frame_tokens, text="Tokens")

salida = tk.Text(frame_salida, width=120, height=20, font=("Courier", 10))
salida.pack(fill=tk.BOTH, expand=True)

panel_tokens = tk.Text(frame_tokens, width=120, height=20, font=("Courier", 10))
panel_tokens.pack(fill=tk.BOTH, expand=True)

ventana.mainloop()
