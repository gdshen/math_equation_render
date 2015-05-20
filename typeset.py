""" 积分号 option + b ∫
    求和号 option + w ∑
"""
from PIL import Image, ImageFont, ImageDraw


class Draw:
    filename = ''
    font_name = 'STIXGeneral.otf'  # 'Courier.dfont'
    character_size = 50

    im = Image.new('L', (500, 500), 255)
    draw = ImageDraw.Draw(im)

    def __init__(self, filename):
        super().__init__()
        with open(filename) as f:
            data = f.readlines()
            for line in data:
                left, height, size, c = line.split(',')
                c = c[:-1]
                if c == '#int':
                    c = '∫'
                if c == '#sum':
                    c = '∑'
                font = ImageFont.truetype(self.font_name, size=int(size))
                self.draw.text((int(left), int(height)), c, font=font)
            self.im.show()
            self.im.close()

if __name__ == '__main__':
    d = Draw('./simple/sample04.txt')