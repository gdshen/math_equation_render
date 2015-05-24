# typeset math equation
> use Python ply library to render simple math equation with LaTeX syntax

## syntax realized
1. B : $$ B $$
2. B : BB
3. B : B_{B}
4. B : B^{B}
5. B : B_^{B}
6. B : (B)

## render image
> use pillow draw module  
1. read date from user input
2. split user input
3. draw data in picture 
4. read until EOF
5. read from file(use readlines)
6. wrap draw as class

## 不同的字体使用的绘制方法不一样，有种被坑的感觉
对于STIX，是默认字体在左下角
1. 先做针对Courier New 这种完美居中的字体的代码
2. 在做针对STIX这种完美左下的字体的代码