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


def t_error(t):
    print("发现非法字符 '{0}'".format(t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()
expression_type = ['p_s_b', 'p_b_tb', 'p_b_t', 'p_b_up_down', 'p_t_up', 'p_b_down', 'p_r_', 'p_b_something',
                   'p_b_blank', 'p_b_lr', 'terminal']


class Symbol:
    def __init__(self, size=50.0, symbol_type="terminal", value=None):
        self.size = size
        self.width = 0
        self.x = 0
        self.y = 0
        self.child = []
        # only leaf node have this value, in the middle node, we use this field to represent the type of the expression
        self.value = value
        self.type = symbol_type

    def __str__(self, *args, **kwargs):
        return "size:{0} x:{1} y:{2} value:{3} type:{4} width:{5}".format(self.size, self.x, 500-self.y,
                                                                          self.value, self.type, self.width)


def shrink_size(size):
    return 0.4 * size


def shrink_y_up(y):
    return -0.2 * y

def shrink_y_down(y):
    return 0.8 * y


def shrink_width(width):
    return 0.6 * width

# todo 针对数字单独做处理
def shrink_number(size):
    return 0.7 * size


l = []


def trans_print(s):
    global l
    # print(s)
    if len(s.child) != 0:
        for i in range(len(s.child)):
            trans_print(s.child[i])
    else:
        l.append([int(s.x), int(s.y), int(s.size), s.value])
        print(s)
        # pass
        # f = open('sample04.txt', 'a')
        # f.write('{0},{1},{2},{3}\n'.format(int(s.x), int(s.y), int(s.size), s.value))
        # f.close()


# 自顶向下分发size 和 y属性
def trans_size(s):
    if len(s.child) == 0:
        return
    if s.type == expression_type[0]:
        s.child[0].size = s.size
        s.child[0].y = s.y
    elif s.type == expression_type[1]:
        s.child[0].size = s.size
        s.child[1].size = s.size
        s.child[0].y = s.y
        s.child[1].y = s.y
    elif s.type == expression_type[2]:
        s.child[0].size = s.size
        s.child[0].y = s.y
    elif s.type == expression_type[3]:
        s.child[0].size = s.size
        s.child[1].size = shrink_size(s.size)
        s.child[2].size = shrink_size(s.size)
        s.child[0].y = s.y
        s.child[1].y = s.y - shrink_y_down(s.size)
        s.child[2].y = s.y + shrink_y_up(s.size)
    elif s.type == expression_type[4]:
        s.child[0].size = s.size
        s.child[1].size = shrink_size(s.size)
        s.child[0].y = s.y
        s.child[1].y = s.y + shrink_y_up(s.size)
    elif s.type == expression_type[5]:
        s.child[0].size = s.size
        s.child[1].size = shrink_size(s.size)
        s.child[0].y = s.y
        s.child[1].y = s.y - shrink_y_down(s.size)
    elif s.type == expression_type[6]:
        s.child[0].size = s.size
        s.child[0].y = s.y
    elif s.type == expression_type[7]:
        s.child[0].size = s.size
        s.child[0].y = s.y
        s.child[0].width = shrink_width(s.child[0].size)
    elif s.type == expression_type[8]:
        s.child[0].size = s.size
        s.child[0].y = s.y
        s.child[0].width = shrink_width(s.child[0].size)
    elif s.type == expression_type[9]:
        s.child[0].size = s.size
        s.child[0].y = s.y
    if len(s.child) != 0:
        for i in range(len(s.child)):
            trans_size(s.child[i])


# bottom-up 分发属性，再处理分发width的时候必须已经分发了size属性，属性之间的相互依赖问题
def trans_width(s):
    if len(s.child) != 0:
        for i in range(len(s.child)):
            trans_width(s.child[i])
    if len(s.child) == 0:
        return
    if s.type == expression_type[0]:
        s.width = s.child[0].width
    elif s.type == expression_type[1]:
        s.width = s.child[0].width + s.child[1].width
    elif s.type == expression_type[2]:
        s.width = s.child[0].width
    elif s.type == expression_type[3]:
        s.width = s.child[0].width + max(s.child[1].width, s.child[2].width)
    elif s.type == expression_type[4]:
        s.width = s.child[0].width + s.child[1].width
    elif s.type == expression_type[5]:
        s.width = s.child[0].width + s.child[1].width
    elif s.type == expression_type[6]:
        s.width = s.child[0].width
    elif s.type == expression_type[7]:
        s.width = s.child[0].width
    elif s.type == expression_type[8]:
        s.width = s.child[0].width
    elif s.type == expression_type[9]:
        s.width = s.child[0].width


# top-down 分发x属性
def trans_x(s):
    if len(s.child) == 0:
        return
    if s.type == expression_type[0]:
        s.child[0].x = s.x
    elif s.type == expression_type[1]:
        s.child[0].x = s.x
        s.child[1].x = s.x + s.child[0].width
    elif s.type == expression_type[2]:
        s.child[0].x = s.x
    elif s.type == expression_type[3]:
        s.child[0].x = s.x
        s.child[1].x = s.x + s.child[0].width
        s.child[2].x = s.x + s.child[0].width
    elif s.type == expression_type[4]:
        s.child[0].x = s.x
        s.child[1].x = s.x + s.child[0].width
    elif s.type == expression_type[5]:
        s.child[0].x = s.x
        s.child[1].x = s.x + s.child[0].width
    elif s.type == expression_type[6]:
        s.child[0].x = s.x
    elif s.type == expression_type[7]:
        s.child[0].x = s.x
    elif s.type == expression_type[8]:
        s.child[0].x = s.x
    elif s.type == expression_type[9]:
        s.child[0].x = s.x
    if len(s.child) != 0:
        for i in range(len(s.child)):
            trans_x(s.child[i])


def p_s_b(t):
    """s : DOLLAR DOLLAR b DOLLAR DOLLAR"""
    t[0] = Symbol(symbol_type=expression_type[0])
    t[0].y = 250.0
    t[0].child.append(t[3])

    trans_size(t[0])
    trans_width(t[0])
    trans_x(t[0])
    trans_print(t[0])


def p_b_tb(t):
    """b : t b"""
    t[0] = Symbol(symbol_type=expression_type[1])
    t[0].child.append(t[1])
    t[0].child.append(t[2])


def p_b_t(t):
    """b : t"""
    t[0] = Symbol(symbol_type=expression_type[2])
    t[0].child.append(t[1])


def p_b_up_down(t):
    """t : r UNDERSCORE CONJUNCTION LSETBRACKET b RSETBRACKET LSETBRACKET b RSETBRACKET"""
    t[0] = Symbol(symbol_type=expression_type[3])
    t[0].child.append(t[1])
    t[0].child.append(t[5])
    t[0].child.append(t[8])


def p_t_up(t):
    """t : r CONJUNCTION LSETBRACKET b RSETBRACKET"""
    t[0] = Symbol(symbol_type=expression_type[4])
    t[0].child.append(t[1])
    t[0].child.append(t[4])


def p_b_down(t):
    """t : r UNDERSCORE LSETBRACKET b RSETBRACKET"""
    t[0] = Symbol(symbol_type=expression_type[5])
    t[0].child.append(t[1])
    t[0].child.append(t[4])


def p_r_(t):
    """t : r"""
    t[0] = Symbol(symbol_type=expression_type[6])
    t[0].child.append(t[1])


def p_b_something(t):
    """r : NAME"""
    t[0] = Symbol(symbol_type=expression_type[7])
    t[0].child.append(Symbol(value=t[1]))


def p_b_blank(t):
    """r : BLANK"""
    t[0] = Symbol(symbol_type=expression_type[8])
    t[0].child.append(Symbol(value=t[1]))


def p_b_lr(t):
    """r : LPAREN b RPAREN"""
    t[0] = Symbol(symbol_type=expression_type[9])
    t[0].child.append(t[2])


def p_error(t):
    print("Syntax error at '%s'" % t.value)


yacc.yacc()

# while 1:
#     try:
#         s = input('math equation > ')  # Use raw_input on Python 2
#         yacc.parse(s)
#     except EOFError:
#         break
yacc.parse("$$abcdefghijk^{d}$$")

from PIL import Image, ImageFont, ImageDraw


class Draw:
    filename = ''
    font_name = 'STIXGeneral.otf'  # 'Courier.dfont'
    character_size = 50

    im = Image.new('L', (500, 500), 255)
    draw = ImageDraw.Draw(im)

    def __init__(self, filename):
        # super().__init__()
        # with open(filename) as f:
        #     data = f.readlines()
        #     for line in data:
        #         left, height, size, c = line.split(',')
        #         c = c[:-1]
        #         if c == '#int':
        #             c = '∫'
        #         if c == '#sum':
        #             c = '∑'
        #         font = ImageFont.truetype(self.font_name, size=int(size))
        #         self.draw.text((int(left), 500-int(height)), c, font=font)
        #     self.im.show()
        #     self.im.close()
        for line in l:
            left, height, size, c = line
            # c = c[:-1]
            # if c == "#int":
            #     c = "∫"
            # if c == "#sum":
            #     c = '∑'
            if ord('a') <= ord(c) <= ord('z'):
                # self.font_name = 'STIXGeneralItalic.otf'
                self.font_name = 'Courier New.ttf'
                # self.font_name = 'consolai.ttf'
            else:
                # self.font_name = 'STIXGeneral.otf'
                self.font_name = 'Courier New.ttf'
                # self.font_name = 'Consolas.ttf'
            font = ImageFont.truetype(self.font_name, size=int(size))
            self.draw.text((int(left), int(height)), c, font=font)
        self.draw.line([0,250,50,250])
        self.draw.line([0,310,50,310])
        self.draw.line([0,360,50,360])
        # self.draw.line([50,250,50,300])
        # self.draw.line([30,250,30,300])
        # self.draw.line([0,300,50,300])
        # self.draw.line([0,215,100,215])
        self.im.show()
        self.im.close()


if __name__ == '__main__':
    d = Draw('sample04.txt')

