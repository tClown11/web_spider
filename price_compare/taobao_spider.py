import requests
import re

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=20)
        r.encoding = r.apparent_encoding  # 转化编码   r.apparent_encoding  根据它的结果转码
        return r.text
    except :
        return ""

def parsePage(inforlist, html):
    try:
        price = re.findall(r'"view_price":"(.*?)"', html)
        title = re.findall(r'"raw_title":"(.*?)"', html)
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
    start_url = 'https://s.taobao.com/search?q=' + product
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44 * i)
            html = getHTMLText(url)
            parsePage(infoList, html)
        except:
            continue
    printview(infoList)

main()