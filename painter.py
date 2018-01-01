import ssl
import time
import urllib
from PIL import Image

import luogu

url = "https://www.luogu.org/paintBoard"
posturl = "https://www.luogu.org/paintBoard/paint"
boaedurl = "https://www.luogu.org/paintBoard/board"

header = {}
header['user-agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
header['accept-encoding'] = "gzip, deflate, br"
header['accept-language'] = "zh,en;q=0.9,zh-CN;q=0.8,ja;q=0.7"
# cookie
header['cookie'] = luogu.get_cookie()
opener = luogu.getOpener(header)

if __name__:
    ssl._create_default_https_context = ssl._create_unverified_context
    print("注意:\n时常更换cookie")
    print("当前cookie: " + header['cookie'])
    ###
    im = Image.open("newhead.jpg")
    w,h = im.size
    count = 0
    failtime = 0
    data = open("data.json","r")
    data = data.read()
    cookie,px,py,height,width = luogu.get_data(data)
    
    print("开始提交")
    for i in range(height,h,1):
        x = px + i    
        for j in range(width,w,1):
            y = py + j
            color = luogu.get_color(im.getpixel((i,j)))
            postdata = luogu.paintData(x,y,color)
            op = opener.open(posturl,postdata)
            data = op.read()
            count += 1
            print("成功提交 "+ str(count) + "次")
            luogu.save(i,j,px,py,cookie)
            print(i,j,x,y,color)
            time.sleep(30) # 等待时间
    print("----------------")
    print("完成提交")
