import ply.lex as lex

tokens = [
    'ID', 'NUM', 'CAD',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN',
    'GT', 'LT', 'EQ',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'COMMA',
    'AMPERSAND'
]

reserved = {
    'int': 'INT', 'float': 'FLOAT', 'char': 'CHAR', 'bool': 'BOOL',
    'if': 'IF', 'else': 'ELSE', 'while': 'WHILE', 'for': 'FOR',
    'scanf': 'SCANF', 'printf': 'PRINTF'
}

tokens += list(reserved.values())

t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_ASSIGN     = r'='
t_GT         = r'>'
t_LT         = r'<'
t_EQ         = r'=='
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_SEMICOLON  = r';'
t_COMMA      = r','
t_AMPERSAND  = r'&'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUM(t):
    r'\d+(\.\d+)?'
    return t

def t_CAD(t):
    r'\".*?\"'
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ✅ Lista global de errores léxicos
errors_lexicos = []

def t_error(t):
    msg = f"Error léxico: '{t.value[0]}' en línea {t.lineno}"
    errors_lexicos.append((msg, t.lineno))
    t.lexer.skip(1)

lexer = lex.lex()
