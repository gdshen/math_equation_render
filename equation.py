import argparse
import ply.lex as lex
import ply.yacc as yacc

tokens = ('ID', 'NUM', 'US', 'CJ', 'LS', 'RS', 'DR', 'BK', 'LP', 'RP', 'INT', 'SUM')

s = ''  # 存储从文件中读取到的字符串
if __name__ == '__main__':
    # 解析命令行参数
    parser_arg = argparse.ArgumentParser()
    parser_arg.add_argument("input_file")
    parser_arg.add_argument('output_file')
    args = parser_arg.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    with open(input_file) as f:
        s = f.readline()
        s = s[:-1]

# define a Symbol class to represent the parse tree node
class Symbol:
    def __init__(self, size=100.0, value=None):
        self.size = size
        self.width = 0
        self.x = 0
        self.y = 0
        self.child = []
        self.value = value

    def __str__(self, *args, **kwargs):
        return "size:{0} x:{1} y:{2} value:{3}  width:{4}" \
            .format(self.size, self.x, 500 - self.y, self.value, self.width)


expression_type = ['p_s_b', 'p_b_tb', 'p_b_t', 'p_t_rbb', 'p_t_up',
                   'p_t_down','p_t_int', 'p_t_sum', 'p_t_r',
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

#
def t_error(t):
    print("在{1}发现非法字符 '{0}'".format(t.value[0], t.lexpos))
    t.lexer.skip(1)

# 构建词法分析器
lexer = lex.lex()

# 以下是语法分析部分
l = []  # 存储节点信息

# 遍历分析树
def trans_print(s):
    if len(s.child) != 0:
        for i in range(len(s.child)):
            trans_print(s.child[i])
    else:
        l.append(str(s.x) + ',' + str(500 - s.y) + ','
                 + str(s.size) + ',' + s.value + '\n')


def shrink_size(size):
    return size * 0.5


def shrink_y_down(size):
    return size * (1 - 0.5)


def shrink_y_up(size):
    return size * (0 / 2)


def shrink_width(size):
    return 0.6 * size


def trans_size(s):
    if len(s.child) == 0:
        return
    s.child[0].size = s.size
    s.child[0].y = s.y
    if s.value == expression_type[1]:
        s.child[1].size = s.size
        s.child[1].y = s.y
    elif s.value == expression_type[3]:
        s.child[1].size = shrink_size(s.size)
        s.child[2].size = shrink_size(s.size)
        s.child[1].y = s.y - shrink_y_down(s.size)
        s.child[2].y = s.y + shrink_y_up(s.size)
    elif s.value == expression_type[4]:
        s.child[1].size = shrink_size(s.size)
        s.child[1].y = s.y + shrink_y_up(s.size)
    elif s.value == expression_type[5]:
        s.child[1].size = shrink_size(s.size)
        s.child[1].y = s.y - shrink_y_down(s.size)
    elif s.value in [expression_type[6], expression_type[7]]:
        s.child[0].y = s.y + 0.1 * s.size  # adjust ∑ ∫ 位置
        s.child[1].size = shrink_size(s.size)
        s.child[2].size = shrink_size(s.size)
        s.child[3].size = s.size
        s.child[1].y = s.y - shrink_y_down(s.size)
        s.child[2].y = s.y + shrink_y_up(s.size)
        s.child[3].y = s.y
        s.child[0].width = shrink_width(s.child[0].size)
    elif s.value in [expression_type[9], expression_type[10], expression_type[11]]:
        s.child[0].width = shrink_width(s.child[0].size)
    elif s.value == expression_type[12]:
        s.child[1].size = s.size
        s.child[2].size = s.size
        s.child[1].y = s.y
        s.child[2].y = s.y
        s.child[0].width = shrink_width(s.child[0].size)
        s.child[2].width = shrink_width(s.child[2].size)
    if len(s.child) != 0:
        for i in range(len(s.child)):
            trans_size(s.child[i])


def trans_width(s):
    if len(s.child) != 0:
        for i in range(len(s.child)):
            trans_width(s.child[i])
    if len(s.child) == 0:
        return
    if s.value in [expression_type[0], expression_type[2], expression_type[8],
                   expression_type[9], expression_type[10], expression_type[11]]:
        s.width = s.child[0].width
    elif s.value in [expression_type[1], expression_type[4], expression_type[5]]:
        s.width = s.child[0].width + s.child[1].width
    elif s.value == expression_type[3]:
        s.width = s.child[0].width + max(s.child[1].width, s.child[2].width)
    elif s.value in [expression_type[6], expression_type[7]]:
        s.width = s.child[0].width +\
                  max(s.child[1].width, s.child[2].width) + s.child[3].width
    elif s.value == expression_type[12]:
        s.width = s.child[0].width + s.child[1].width + s.child[2].width


def trans_x(s):
    if len(s.child) == 0:
        return
    s.child[0].x = s.x
    if s.value in [expression_type[1], expression_type[4], expression_type[5]]:
        s.child[1].x = s.x + s.child[0].width
    elif s.value == expression_type[3]:
        s.child[1].x = s.x + s.child[0].width
        s.child[2].x = s.x + s.child[0].width
    elif s.value in [expression_type[6], expression_type[7]]:
        s.child[1].x = s.x + s.child[0].width
        s.child[2].x = s.x + s.child[0].width
        s.child[3].x = s.x + s.child[0].width +\
                       max(s.child[1].width, s.child[2].width)
    elif s.value == expression_type[12]:
        s.child[1].x = s.x + s.child[0].width
        s.child[2].x = s.x + s.child[0].width + s.child[1].width
    if len(s.child) != 0:
        for i in range(len(s.child)):
            trans_x(s.child[i])


def p_s_b(p):
    """s : DR DR b DR DR"""
    p[0] = Symbol(value=expression_type[0])
    p[0].child.append(p[3])
    p[0].y = 250

    trans_size(p[0])
    trans_width(p[0])
    trans_x(p[0])
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


def p_error(p):
    if p:
        print("Syntax error at token {0}".format(p.type))
        # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()
parser.parse(s)

with open(output_file, 'w') as f:
    for line in l:
        f.writelines(line)
