import argparse
from PIL import Image, ImageFont, ImageDraw


def draw(file_name):
    font_name = 'Courier New.ttf'
    im = Image.new('L', (500, 500), 255)
    drawer = ImageDraw.Draw(im)
    with open(file_name) as f:
        l = f.readlines()
        print(l)
        for line in l:
            left, height, size, c = line.split(',')
            c = c[:-1]
            if c == "#int":
                c = "∫"
            if c == "#sum":
                c = '∑'
            font = ImageFont.truetype(font_name, size=int(float(size)))
            drawer.text((int(float(left)), int(float(height))), c, font=font)
    # drawer.line([0, 250, 50, 250])
    im.show()
    im.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    draw(filename)
