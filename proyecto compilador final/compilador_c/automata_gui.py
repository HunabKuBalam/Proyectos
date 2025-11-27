import tkinter as tk
import math

def draw_automata_window(transitions):
    """
    Abre una ventana independiente para visualizar el autómata.
    transitions: lista de (src, dst, label)
    """
    ventana = tk.Toplevel()
    ventana.title("Visualización del Autómata")
    ventana.geometry("1000x700")

    canvas = tk.Canvas(ventana, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)

    # Estados únicos
    estados = list(set([src for src, _, _ in transitions] + [dst for _, dst, _ in transitions]))

    # Distribuir estados en círculo
    n = len(estados)
    radio = 250
    centro_x, centro_y = 500, 350
    posiciones = {}
    for i, estado in enumerate(estados):
        ang = 2 * math.pi * i / n
        x = centro_x + radio * math.cos(ang)
        y = centro_y + radio * math.sin(ang)
        posiciones[estado] = (x, y)
        canvas.create_oval(x-30, y-30, x+30, y+30, fill="lightblue")
        canvas.create_text(x, y, text=estado, font=("Arial", 10, "bold"))

    # Dibujar transiciones con etiquetas desplazadas
    offset = 15  # separación vertical para las etiquetas
    for idx, (src, dst, label) in enumerate(transitions):
        x1, y1 = posiciones[src]
        x2, y2 = posiciones[dst]
        canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)

        # Calcular punto medio
        xm, ym = (x1+x2)/2, (y1+y2)/2

        # Alternar desplazamiento para evitar superposición
        dy = offset if idx % 2 == 0 else -offset
        canvas.create_text(xm, ym+dy, text=label, font=("Arial", 9), fill="red")

    ventana.mainloop()
