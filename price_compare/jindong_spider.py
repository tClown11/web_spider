import requests
import re

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=20)
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def parseText(inforlist, html):
    try:
        price = re.findall(r'<div class="p-price">.*?<i>(.*?)</i>', html, re.S)
        title = re.findall(r'<div class="p-img">.*?title="(.*?)"', html, re.S)
        for i in range(len(price)):
            inforlist.append([price[i], title[i]])
    except:
        print("")

def printview(inforlist):
    tplt = "{:4}\t{:8}\t{:16}"
    print(tplt.format("序号", "价格", "商品名称"))
    count = 0
    for g in inforlist:
        count = count + 1
        print(tplt.format(count, g[0], g[1]))

def main():
    product = input("请输入你要查找的物品：")
    depth = 3    #爬取前三页
    start_url = 'https://search.jd.com/search?keyword=' + product + '&enc=utf-8'
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&page=' + str(1 + 2 *(i - 1)) + '&s=' + str(52 * i)
            html = getHTMLText(url)
            parseText(infoList, html)
        except:
            continue
    printview(infoList)

main()