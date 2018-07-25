# coding=utf-8
import urllib.parse
import requests
import re

def search(url):
    try:
        r = requests.get(url, timeout=20)
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("")


def build_url():
    #infolist = []
    #keyword = '权力的游戏'.encode('gb2312')
    keyword  = input("请输入要查找的电影名称：(请输入中文否则无法找到您想要的)").encode('gb2312')
    quote = urllib.parse.quote(keyword)
    start_url = 'http://s.ygdy8.com/plus/so.php?kwtype=0&searchtype=title&keyword=' + quote
    start_html = search(start_url)
    #print(start_html)
    try:
        target = re.findall(r"<b><a href='(/html[^\s]*?.html)", start_html, re.S)
        for i in target:
            second_url = 'http://s.ygdy8.com' + i
            second_html = search(second_url)
            movic = re.findall(r'href="[a-zA-z]+://[^\s]*?[mp4,avi,rmvb,mkv,wmv]"', second_html)

            printview(movic)
            print("--------------------------------------------")
    except:
        print("")


def printview(inforlist):
    tplt = "{:4}\t{:16}"
    print(tplt.format("序号", "资源"))
    count = 0
    for g in inforlist:
        count = count + 1
        print(tplt.format(count, g))

def main():
    build_url()
    #printview(movic)

main()
#ftp://ygdy8:ygdy8@yg45.dydytt.net:3110/阳光电影www.ygdy8.com.头号玩家.BD.720p.国英双语双字.mkv