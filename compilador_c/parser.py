import ply.yacc as yacc
from lexer import tokens
from semantic import check_declaration, check_assignment

symbol_table = {}

def p_program(p):
    '''program : statement program
               | declaration program
               | empty'''
    pass

def p_declaration(p):
    '''declaration : type id_list SEMICOLON'''
    for var in p[2]:
        symbol_table[var] = p[1]

def p_type_int(p):    'type : INT';    p[0] = p[1]
def p_type_float(p):  'type : FLOAT';  p[0] = p[1]
def p_type_char(p):   'type : CHAR';   p[0] = p[1]
def p_type_bool(p):   'type : BOOL';   p[0] = p[1]

def p_id_list(p):
    '''id_list : ID
               | ID COMMA id_list'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

def p_statement(p):
    '''statement : assignment SEMICOLON
                 | conditional
                 | loop
                 | io SEMICOLON'''
    pass

def p_assignment(p):
    '''assignment : ID ASSIGN expression'''
    expected_type = symbol_table.get(p[1], None)
    check_declaration(p[1], symbol_table, p.lineno(1))
    check_assignment(p[1], expected_type, symbol_table, p.lineno(1))

def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | term'''
    pass

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    pass

def p_factor(p):
    '''factor : ID
              | NUM
              | LPAREN expression RPAREN'''
    pass

def p_expression_relational(p):
    '''expression : expression GT expression
                  | expression LT expression
                  | expression EQ expression'''
    pass

def p_conditional(p):
    '''conditional : IF LPAREN expression RPAREN block
                   | IF LPAREN expression RPAREN block ELSE block'''
    pass

def p_loop(p):
    '''loop : WHILE LPAREN expression RPAREN block
            | FOR LPAREN assignment SEMICOLON expression SEMICOLON assignment RPAREN block'''
    pass

def p_io(p):
    '''io : PRINTF LPAREN argument RPAREN
          | SCANF LPAREN argument RPAREN'''
    pass

def p_argument(p):
    '''argument : CAD COMMA ID
                | CAD COMMA AMPERSAND ID
                | ID'''
    pass

def p_block(p):
    '''block : LBRACE program RBRACE'''
    pass

def p_empty(p): 'empty :'; pass

def p_error(p):
    from gui import log_error
    lineno = p.lineno if p else 1
    msg = f"Error sintáctico en '{p.value}' línea {lineno}" if p else "Error sintáctico inesperado"
    log_error(msg, lineno)

parser = yacc.yacc()
