import telnetlib

import requests
import re


url = 'http://www.xicidaili.com/wt'
proxy_list = []
proxy_success = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
}
#寻找网上的免费代理，并获取到代理的ip及端口号
def proxies_list(url, proxy_list):
    page = requests.get(url, headers=headers)
    #soup = BeautifulSoup(page.text, 'lxml')
    ul_list = re.findall(r'<tr[\s\S]*?>([\s\S]*?)</tr>',page.text)
    #ul_list = soup.find_all('tr', limit=30)
    #print(len(ul_list))
    for i in range(1, 20):
    #for i in range(1, len(ul_list)):
        line = ul_list[i].split('\n')
        ip = line[2][10:-5]
        port = line[3][10:-5]
        address = ip + ':' + port
        proxy_list.append(address)
    return proxy_list


#测试免费代理的可用性并保存可用代理
def parse_ip(target_text):
    for i in target_text:
        ad, port = i.split(":")
        try:
            telnetlib.Telnet(ad, port=port, timeout=20)
        except:
            print("失败")

        else:
            print("成功")
            get_url(ad, i)


#尝试get请求
def get_url(ad, i):
    proxies = {
        'http': 'http://' + ad,
    }

    try:
        response = requests.get('http://httpbin.org/get', proxies=proxies)
        print(response.text)
        if response.status_code == 200:
            proxy_success.append(i)
    except:
        print('连接不成功')





def main():
    target_1 = proxies_list(url, proxy_list)
    parse_ip(target_1)
    print(proxy_success)


if __name__ == "__main__":
    main()

pass