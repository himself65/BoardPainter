from PIL import Image

import luogu

data = open("data_1.json","w+")
im = Image.open("newhead.jpg")
w,h = im.size

startx=190
starty=90
data.write("[")
for i in range(0,h,1):
    x = startx + i
    for j in range(0,w,1):
        y = starty + j
        color = luogu.get_color(im.getpixel((i,j)))
        content = "[{0},{1},{2}]".format(str(y),str(x),str(color))
        if (i!=h-1 or j < w-1):
            content+= ','
        size = data.write(content)
data.write("]")
data.close()
