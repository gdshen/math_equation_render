tokens = ('ID', 'NUM', 'US', 'CJ', 'LS', 'RS', 'DR', 'BK', 'LP', 'RP', 'INT', 'SUM')

import ply.lex as lex
import ply.yacc as yacc


# todo to use different resolve method in num and id
# define a Symbol class to represent the parse tree node
class Symbol:
    def __init__(self, size=100.0, value=None):
        self.size = size
        self.width = 0
        self.x = 0
        self.y = 0
        self.child = []
        # only leaf node have this value, in the middle node, we use this field to represent the type of the expression
        self.value = value

    def __str__(self, *args, **kwargs):
        return "size:{0} x:{1} y:{2} value:{3}  width:{4}".format(self.size, self.x, 500 - self.y, self.value,
                                                                  self.width)


expression_type = ['p_s_b', 'p_b_tb', 'p_b_t', 'p_t_rbb', 'p_t_up', 'p_t_down', 'p_t_int', 'p_t_sum', 'p_t_r',
                   'p_r_id', 'p_r_num', 'p_r_blank', 'p_r_b']

# 正则表达式的特殊字符需要转义
t_ID = r'[a-z]'
t_NUM = r'\d'
t_US = r'\_'
t_CJ = r'\^'
t_LS = r'\{'
t_RS = r'\}'
t_DR = r'\$'
t_BK = r'\\blank'
t_LP = r'\('
t_RP = r'\)'
t_INT = r'\\int'
t_SUM = r'\\sum'

# 空白字符忽略
t_ignore = " \t"

l = []

# 遍历分析树
def trans_print(s):
    global l
    # print(s)
    if len(s.child) != 0:
        for i in range(len(s.child)):
            trans_print(s.child[i])
    else:
        l.append([int(s.x), int(s.y), int(s.size), s.value])
        print(s)


def t_error(t):
    print("发现非法字符 '{0}'".format(t.value[0]))
    t.lexer.skip(1)

# 构建词法分析器
lexer = lex.lex()

# todo 计算属性

def p_s_b(p):
    """s : DR DR b DR DR"""
    p[0] = Symbol(value=expression_type[0])
    p[0].child.append(p[3])
    trans_print(p[0])


def p_b_tb(p):
    """b : t b"""
    p[0] = Symbol(value=expression_type[1])
    p[0].child.append(p[1])
    p[0].child.append(p[2])


def p_b_t(p):
    """b : t"""
    p[0] = Symbol(value=expression_type[2])
    p[0].child.append(p[1])


def p_t_rbb(p):
    """t : r US CJ LS b RS LS b RS"""
    p[0] = Symbol(value=expression_type[3])
    p[0].child.append(p[1])
    p[0].child.append(p[5])
    p[0].child.append(p[8])


def p_t_up(p):
    """t : r CJ LS b RS"""
    p[0] = Symbol(value=expression_type[4])
    p[0].child.append(p[1])
    p[0].child.append(p[4])


def p_t_down(p):
    """t : r US LS b RS"""
    p[0] = Symbol(value=expression_type[5])
    p[0].child.append(p[1])
    p[0].child.append(p[4])


def p_t_int(p):
    """t : INT LS b RS LS b RS LS b RS"""
    p[0] = Symbol(value=expression_type[6])
    p[0].child.append(Symbol(value='#int'))
    p[0].child.append(p[3])
    p[0].child.append(p[6])
    p[0].child.append(p[9])


def p_t_sum(p):
    """t : SUM LS b RS LS b RS LS b RS"""
    p[0] = Symbol(value=expression_type[7])
    p[0].child.append(Symbol(value='#sum'))
    p[0].child.append(p[3])
    p[0].child.append(p[6])
    p[0].child.append(p[9])


def p_t_r(p):
    """t : r"""
    p[0] = Symbol(value=expression_type[8])
    p[0].child.append(p[1])


def p_r_id(p):
    """r : ID"""
    p[0] = Symbol(value=expression_type[9])
    p[0].child.append(Symbol(value=p[1]))


def p_r_num(p):
    """r : NUM"""
    p[0] = Symbol(value=expression_type[10])
    p[0].child.append(Symbol(value=p[1]))


def p_r_blank(p):
    """r : BK"""
    p[0] = Symbol(value=expression_type[11])
    p[0].child.append(Symbol(value=p[1]))


def p_r_b(p):
    """r : LP b RP"""
    p[0] = Symbol(value=expression_type[12])
    p[0].child.append(Symbol(value=p[1]))
    p[0].child.append(p[2])
    p[0].child.append(Symbol(value=p[3]))


def p_error(t):
    print("Syntax error at '%s'" % t.value)


yacc.yacc()
yacc.parse("$$a^{b}$$")
