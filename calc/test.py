__author__ = 'shen'
import ply.lex as lex
import ply.yacc as yacc
from matplotlib import pyplot as plt

if __name__ == "__main__":
    s = r'hello\n'
    print(s)
    a = range(1, 10)
    b = a
    plt.plot(a, b)
    plt.xlabel("这里是x轴")
    plt.ylabel("这里是y轴")
    plt.show()