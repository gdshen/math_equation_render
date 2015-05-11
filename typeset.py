from PIL import Image, ImageDraw, ImageFont

im = Image.new("L", (500, 500), 255)
draw = ImageDraw.Draw(im)
fontC = ImageFont.truetype("STIXGeneralItalic.otf", 50)
fontN = ImageFont.truetype("STIXGeneral.otf", 30)
# fontC = ImageFont.truetype("Consolas.ttf",50)
# string = 'abcdefghigklmnopqrstuvwxyz'
number = '2'
string = 'a = b + c'
draw.text((100, 100), string, font=fontC)
draw.text((125, 100), number, font=fontN)
im.show()
