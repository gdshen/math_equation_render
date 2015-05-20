__author__ = 'shen'

class Symbol:
    def __init__(self):
        self.position = "hello world"


a = Symbol()
b = Symbol()

print(id(a.position))
print(id(b.position))

