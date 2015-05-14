# -----------------------------------------------------------------------------
# simple_equation.py
#
# A simple math render with python ply  -- all in one file.
# -----------------------------------------------------------------------------

import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'NAME', 'UNDERSCORE', 'CONJUNCTION', 'LSETBRACKET', 'RSETBRACKET', 'DOLLAR', 'BLANK', 'LPAREN', 'RPAREN'
)

# Tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSETBRACKET = r'\{'
t_RSETBRACKET = r'\}'
t_UNDERSCORE = r'\_'
t_CONJUNCTION = r'\^'
t_DOLLAR = r'\$'
t_BLANK = r'\\blank'
t_NAME = r'[a-z0-9]'
t_ignore = " \t"


class Symbol:
    position = 0
    size = 50

    def __init__(self, position=0, size=50):
        super().__init__()
        self.size = size
        self.position = position

    def __str__(self, *args, **kwargs):
        return "position {0}; size {1}".format(self.position, self.size)


def t_error(t):
    print("发现非法字符 '{0}'".format(t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()


def p_s_b(t):
    's : DOLLAR DOLLAR b DOLLAR DOLLAR'
    # t[0] = Symbol(position=t[3].position+1)
    t[0] = ('$', '$', t[3], '$', '$')
    print(t[0])


def p_b_tb(t):
    """b : t b"""
    t[0] = (t[1], t[2])
    print(t[0])


def p_b_t(t):
    """b : t"""
    # t[0] = Symbol(position=t[1].position + 1, size=t[1].size + 1)
    # print(t[0])
    t[0] = t[1]
    print(t[0])


def p_b_up_down(t):
    't : r UNDERSCORE CONJUNCTION LSETBRACKET b RSETBRACKET LSETBRACKET b RSETBRACKET'
    # print(t[])
    t[0] = (t[1], '_', '^', '{', t[5], '}', '{', t[8], '}')
    print(t[0])


def p_t_up(t):
    't : r CONJUNCTION LSETBRACKET b RSETBRACKET'
    t[0] = (t[1], '^', '{', t[4], '}')
    print(t[0])


def p_b_down(t):
    't : r UNDERSCORE LSETBRACKET b RSETBRACKET'
    t[0] = (t[1], '_', '{', t[4], '}')
    print(t[0])


def p_r_(t):
    't : r'
    # t[0] = Symbol(position=t[1].position + 1, size=t[1].size)
    # print(t[0])
    t[0] = t[1]
    print(t[0])


def p_b_something(t):
    '''r : NAME'''
    # t[1] = Symbol()
    # t[0] = Symbol(position=t[1].position, size=t[1].size)
    # print(t[0])
    t[0] = t[1]
    print(t[0])


def p_b_blank(t):
    '''r : BLANK'''
    t[0] = t[1]
    print(t[0])


def p_b_lr(t):
    """r : LPAREN b RPAREN"""
    t[0] = ('(', t[1], ')')
    print(t[0])


def p_error(t):
    print("Syntax error at '%s'" % t.value)


yacc.yacc()

while 1:
    try:
        s = input('math equation > ')  # Use raw_input on Python 2
    except EOFError:
        break
    yacc.parse(s)
