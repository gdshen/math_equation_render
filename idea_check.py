__author__ = 'shen'
tokens = ('NUMBER',)

t_NUMBER = r'\d+'
t_ignore = ' \t'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("发现非法字符 '{0}'".format(t.value[0]))
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lexer = lex.lex()

def p_number(p):
    's : t r '

def p_t(p):
    't : NUMBER'
    p[0] = p[1]

def p_s(p):
    'r : NUMBER'
    print(p[-1])

import ply.yacc as yacc

yacc.yacc()

yacc.parse('2 3')