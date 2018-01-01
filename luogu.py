import gzip
import http.cookiejar
import os
import ssl
import time
import json
from urllib import parse, request
from colorsys import rgb_to_hsv

fileLocation = "data.json"
imageLocation = "newhead.jpg"
colors = {
    (0, 0, 0):0,
    (255, 255, 255):1,
    (170, 170, 170):2,
    (85, 85, 85):3,
    (254, 211, 199):4,
    (255, 196, 206):5,
    (250, 172, 142):6,
    (255, 139, 131):7,
    (244, 67, 54):8,
    (233, 30, 99):9,
    (226, 102, 158):10,
    (156, 39, 176):11,
    (103, 58, 183):12,
    (63, 81, 181):13,
    (0, 70, 112):14,
    (5, 113, 151):15,
    (33, 150, 243):16,
    (0, 188, 212):17,
    (59, 229, 219):18,
    (151, 253, 220):19,
    (22, 115, 0):20,
    (55, 169, 60):21,
    (137, 230, 66):22,
    (215, 255, 7):23,
    (255, 246, 209):24,
    (248, 203, 140):25,
    (255, 235, 59):26,
    (255, 193, 7):27,
    (255, 152, 0):28,
    (255, 87, 34):29,
    (184, 63, 39):30,
    (121, 85, 72):31,
}

def get_color(pixel):
    return min_color_diff(pixel, colors)[1]

def ungzip(data):
    try:
        print("正在解压")
        data = gzip.decompress(data)
        print("解压完成")
    except:
        print("解压失败")
    return data

def getOpener(head):
    cj = http.cookiejar.CookieJar()
    pro = request.HTTPCookieProcessor(cj)
    opener = request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

def paintData(x, y, color):
    postDict = {
        'x' : str(x),
        'y' : str(y),
        'color' : str(color)
    }
    postData = parse.urlencode(postDict).encode()
    return postData

# 接受op.read内容
def check(data):
    data = json.loads(data)
    if (data['status'] == 200):
        return True
    else:
        return False

def paintOnLine(x,y,color):
    """ 此函数已经废弃，本意是画直线 """
    postData = paintData(x,y,color)
    op = opener.open(posturl,postData)
    while check(op.read()) != True:
        postData = paintData(x,y,color)
        op = opener.open(posturl,postData)

def paintline(x0,y0,x1,y1,color): # 实现自动化画线？？
    """ 此函数已经废弃，本意是画直线 """
    dx = abs(x1-x0)
    dy = abs(y1-y0)
    if x0 < x1:
        sx = 1
    else:
        sx = -1
    if y0 < y1:
        sy = 1
    else:
        sy = -1
    if dx > dy:
        err = dx
    else:
        err = -dy
    err = err / 2
    paintOnLine(x0,y0,color)
    while (x0 != x1 and y0 != y1):
        e2 = err
        if e2 > -dx:
            err = err - dy
            x0 = x0 + sx
        if e2 < dy:
            err = err + dx
            y0 = y0 + sy
        time.sleep(16) # 此处等待16秒，多等一会儿
        paintOnLine(x0,y0,color)

def to_hsv( color ): 
    return rgb_to_hsv(*[x/255.0 for x in color])

def color_dist( c1, c2):
    return sum( (a-b)**2 for a,b in zip(to_hsv(c1),to_hsv(c2)) )

def min_color_diff( color_to_match, colors):
    """ 返回字典中最小颜色差值的值"""
    return min(
        (color_dist(color_to_match, test), colors[test])
        for test in colors)

def get_data(data):
    data = json.loads(data)
    return data["cookie"],data["x"],data["y"],data["height"],data["width"]

def save(height,width,x,y,cookie):
    """ 保存数据到本地 """
    data = {
        "cookie":cookie,
        "x":x,
        "y":y,
        "height":height,
        "width":width
    }
    data = json.dumps(data)
    try:
        f = open(fileLocation,'w+')
        f.write(data)
    except:
        print("储存错误")
    finally:
        f.close()
    
def get_cookie():
    f = open(fileLocation,'r')
    data = json.load(f)
    return data["cookie"]