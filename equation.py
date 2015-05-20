# -----------------------------------------------------------------------------
# equation.py
#
# A simple math equation render with python ply  -- all in one file.
# -----------------------------------------------------------------------------

tokens = (
    'NAME', 'NUMBER', 'UNDERSCORE', 'CONJUNCTION', 'LSETBRACKET', 'RSETBRACKET', 'DOLLAR', "BACKSLASH",
    'SPACE', 'LPAREN', 'RPAREN', 'INT', 'SUM'
)

# Tokens

# 正则表达式的特殊字符需要转义
t_BACKSLASH = r'\\'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSETBRACKET = r'\{'
t_RSETBRACKET = r'\}'
t_UNDERSCORE = r'\_'
t_CONJUNCTION = r'\^'
t_DOLLAR = r'\$'
t_SPACE = r'\s'
t_INT = r'\\int'
t_SUM = r'\\sum'
t_NAME = r'[a-z][a-z0-9]*'


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = "\t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("发现非法字符 '{0}'".format(t.value[0]))
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex

lexer = lex.lex()


def p_s_b(t):
    's : DOLLAR DOLLAR b DOLLAR DOLLAR'
    print(t[3])


def p_b_tb(t):
    '''b : t b
    | t'''
    print(t[1])


def p_b_up_down(t):
    't : r UNDERSCORE CONJUNCTION LSETBRACKET b RSETBRACKET LSETBRACKET b RSETBRACKET'
    print(t[5])


def p_t_up(t):
    't : r CONJUNCTION LSETBRACKET b RSETBRACKET'
    print(t[4])


def p_b_down(t):
    't : r UNDERSCORE LSETBRACKET b RSETBRACKET'
    print(t[4])


def p_b_int(t):
    't : INT LSETBRACKET b RSETBRACKET LSETBRACKET b RSETBRACKET LSETBRACKET b RSETBRACKET'
    print(t[3])


def p_b_sum(t):
    't : SUM LSETBRACKET b RSETBRACKET LSETBRACKET b RSETBRACKET LSETBRACKET b RSETBRACKET'
    print(t[3])


def p_r_(t):
    't : r'
    print(t[1])


def p_b_something(t):
    '''r : NAME
    | NUMBER
    | SPACE
    | LPAREN b RPAREN'''
    print(t[1])


def p_error(t):
    print("Syntax error at '%s'" % t.value)


import ply.yacc as yacc

yacc.yacc()
while 1:
    try:
        s = input('math equation > ')
    except EOFError:
        break
    yacc.parse(s)
