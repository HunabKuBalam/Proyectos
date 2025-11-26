from graphviz import Digraph

def draw_tree_image(root, filename="arbol_sintactico"):
    """
    Genera un grafo del árbol sintáctico y lo guarda como imagen PNG.
    Retorna la ruta del archivo generado.
    """
    dot = Digraph(comment="Árbol sintáctico")
    visited = set()

    def add_nodes(node):
        if node is None or id(node) in visited:
            return
        visited.add(id(node))
        dot.node(str(id(node)), node.label)
        for child in getattr(node, "children", []):
            dot.node(str(id(child)), child.label)
            dot.edge(str(id(node)), str(id(child)))
            add_nodes(child)

    add_nodes(root)
    output_path = dot.render(filename, format="png", cleanup=True)
    return output_path


def draw_automata(transitions, filename="automata_proceso"):
    """
    Genera un grafo orientado del autómata del proceso y lo guarda como PNG.
    transitions: lista de (src, dst, label)
    Retorna la ruta del archivo generado.
    """
    dot = Digraph(comment="Autómata del proceso")
    dot.attr(rankdir="LR", fontsize="12", fontname="Arial")
    dot.attr("node", shape="circle", fontname="Courier")
    dot.attr("edge", fontname="Courier")

    nodes = set()
    for src, dst, label in transitions:
        nodes.add(src)
        nodes.add(dst)

    for n in nodes:
        dot.node(n)

    # Opcional: marcar inicio y fin
    if "start" in nodes:
        dot.node("start", shape="doublecircle")
    if "end" in nodes:
        dot.node("end", shape="doublecircle")

    for src, dst, label in transitions:
        dot.edge(src, dst, label=label)

    output_path = dot.render(filename, format="png", cleanup=True)
    return output_path
