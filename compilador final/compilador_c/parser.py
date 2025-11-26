import ply.yacc as yacc
from lexer import tokens
from semantic import check_declaration, check_assignment, errors_semanticos

# Tabla de símbolos
symbol_table = {}

# Errores sintácticos
errors_sintacticos = []

# Registro del autómata (lista de transiciones)
# Cada item: (estado_origen, estado_destino, etiqueta)
automata_transitions = []

def add_edge(src, dst, label):
    automata_transitions.append((src, dst, label))

# Clase para nodos (si quieres seguir usando árbol internamente)
class Node:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children if children else []
    def __repr__(self):
        return self.label

# --------- Gramática e instrumentación ---------

def p_program_concat(p):
    '''program : program unit'''
    add_edge("start", "program", "program+unit")
    p[0] = Node("program", [p[1], p[2]])

def p_program_unit(p):
    '''program : unit'''
    add_edge("start", "program", "unit")
    p[0] = Node("program", [p[1]])

def p_unit(p):
    '''unit : statement
            | declaration'''
    label = "stmt" if isinstance(p[1], Node) and p[1].label == "stmt" else "decl"
    add_edge("program", label, "unit->" + label)
    p[0] = p[1]

def p_declaration(p):
    '''declaration : type id_list SEMICOLON'''
    add_edge("program", "decl", "type id_list ;")
    for var in p[2]:
        symbol_table[var] = p[1]
    p[0] = Node(f"decl({p[1]})", [Node(v) for v in p[2]])

def p_type_int(p): 'type : INT'; p[0] = 'INT'
def p_type_float(p): 'type : FLOAT'; p[0] = 'FLOAT'
def p_type_char(p): 'type : CHAR'; p[0] = 'CHAR'
def p_type_bool(p): 'type : BOOL'; p[0] = 'BOOL'

def p_id_list_single(p):
    '''id_list : ID'''
    add_edge("decl", "decl", "ID")
    p[0] = [p[1]]

def p_id_list_multi(p):
    '''id_list : ID COMMA id_list'''
    add_edge("decl", "decl", "ID , id_list")
    p[0] = [p[1]] + p[3]

def p_statement(p):
    '''statement : assignment SEMICOLON
                 | conditional
                 | loop
                 | io SEMICOLON'''
    # Detectar tipo de statement
    lbl = "assign" if isinstance(p[1], Node) and p[1].label == "assign" else p[1].label
    add_edge("program", "stmt", lbl)
    p[0] = Node("stmt", [p[1]])

def p_assignment(p):
    '''assignment : ID ASSIGN expression'''
    var = p[1]
    expected_type = symbol_table.get(var, None)
    check_declaration(var, symbol_table, p.lineno(1))
    check_assignment(var, expected_type, symbol_table, p.lineno(1))
    add_edge("stmt", "assign", f"{var} = expr")
    p[0] = Node("assign", [Node(var), p[3]])

def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    add_edge("expr", "expr", p[2])  # + o -
    p[0] = Node(p[2], [p[1], p[3]])

def p_expression_term(p):
    '''expression : term'''
    add_edge("assign", "expr", "term")
    p[0] = p[1]

def p_term_binop(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    add_edge("term", "term", p[2])  # * o /
    p[0] = Node(p[2], [p[1], p[3]])

def p_term_factor(p):
    '''term : factor'''
    add_edge("expr", "term", "factor")
    p[0] = p[1]

def p_factor_id(p):
    '''factor : ID'''
    add_edge("term", "factor", "ID")
    p[0] = Node(f"id({p[1]})")

def p_factor_num(p):
    '''factor : NUM'''
    add_edge("term", "factor", "NUM")
    p[0] = Node(f"num({p[1]})")

def p_factor_group(p):
    '''factor : LPAREN expression RPAREN'''
    add_edge("term", "factor", "( expr )")
    p[0] = Node("group", [p[2]])

def p_expression_relational(p):
    '''expression : expression GT expression
                  | expression LT expression
                  | expression EQ expression'''
    add_edge("expr", "expr", p[2])  # > < ==
    p[0] = Node(p[2], [p[1], p[3]])

def p_conditional_if(p):
    '''conditional : IF LPAREN expression RPAREN block'''
    add_edge("stmt", "cond", "IF ( expr ) block")
    p[0] = Node("if", [p[3], p[5]])

def p_conditional_if_else(p):
    '''conditional : IF LPAREN expression RPAREN block ELSE block'''
    add_edge("stmt", "cond", "IF ( expr ) block ELSE block")
    p[0] = Node("ifelse", [p[3], p[5], p[7]])

def p_loop_while(p):
    '''loop : WHILE LPAREN expression RPAREN block'''
    add_edge("stmt", "loop", "WHILE ( expr ) block")
    p[0] = Node("while", [p[3], p[5]])

def p_loop_for(p):
    '''loop : FOR LPAREN assignment SEMICOLON expression SEMICOLON assignment RPAREN block'''
    add_edge("stmt", "loop", "FOR (...)")
    p[0] = Node("for", [p[3], p[5], p[7], p[9]])

def p_io_printf(p):
    '''io : PRINTF LPAREN argument RPAREN'''
    add_edge("stmt", "io", "PRINTF ( args )")
    p[0] = Node("printf", [p[3]])

def p_io_scanf(p):
    '''io : SCANF LPAREN argument RPAREN'''
    add_edge("stmt", "io", "SCANF ( args )")
    p[0] = Node("scanf", [p[3]])

def p_argument_format_id(p):
    '''argument : CAD COMMA ID'''
    add_edge("io", "io", "CAD , ID")
    p[0] = Node("args", [Node(f"str({p[1]})"), Node(f"id({p[3]})")])

def p_argument_format_addr(p):
    '''argument : CAD COMMA AMPERSAND ID'''
    add_edge("io", "io", "CAD , & ID")
    p[0] = Node("args", [Node(f"str({p[1]})"), Node(f"&id({p[4]})")])

def p_argument_id(p):
    '''argument : ID'''
    add_edge("io", "io", "ID")
    p[0] = Node(f"id({p[1]})")

def p_block(p):
    '''block : LBRACE program RBRACE'''
    add_edge("cond", "block", "{ program }")
    add_edge("loop", "block", "{ program }")
    p[0] = Node("block", [p[2]])

def p_error(p):
    lineno = p.lineno if p else 1
    msg = f"Error sintáctico en '{p.value}' línea {lineno}" if p else "Error sintáctico inesperado"
    errors_sintacticos.append((msg, lineno))
    add_edge("error", "error", msg)

# Construir parser
parser = yacc.yacc()
