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


def t_error(t):
    print("发现非法字符 '{0}'".format(t.value[0]))
    t.lexer.skip(1)

# 构建词法分析器
lexer = lex.lex()

# todo 计算属性

def p_s_b(p):
    """s : DR DR b DR DR"""
    pass


def p_b_tb(p):
    """b : t b"""
    pass


def p_b_t(p):
    """b : t"""
    pass


def p_t_rbb(p):
    """t : r US CJ LS b RS LS b RS"""
    pass


def p_t_up(p):
    """t : r CJ LS b RS"""
    pass


def p_t_down(p):
    """t : r US LS b RS"""
    pass


def p_t_int(p):
    """t : INT LS b RS LS b RS LS b RS"""
    pass


def p_t_sum(p):
    """t : SUM LS b RS LS b RS LS b RS"""
    pass


def p_t_r(p):
    """t : r"""
    pass


def p_r_id(p):
    """r : ID"""
    pass


def p_r_num(p):
    """r : NUM"""
    pass


def p_r_blank(p):
    """r : BK"""
    pass


def p_r_b(p):
    """r : LP b RP"""
    pass


def p_error(t):
    print("Syntax error at '%s'" % t.value)


yacc.yacc()
yacc.parse("$$a$$")
