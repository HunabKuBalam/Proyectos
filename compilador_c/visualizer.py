from graphviz import Digraph

class Node:
    def __init__(self, label):
        self.label = label
        self.children = []

def draw_tree(root):
    dot = Digraph()
    def add_nodes(node):
        dot.node(str(id(node)), node.label)
        for child in node.children:
            dot.node(str(id(child)), child.label)
            dot.edge(str(id(node)), str(id(child)))
            add_nodes(child)
    add_nodes(root)
    dot.render('arbol_derivacion', view=True)
