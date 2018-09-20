import threading
import time

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.lagou

#proxy = {"https": 'https://%s' %input('请输入代理IP:')}

def get_json(keyword, page):
    data = {
        'kd': keyword,
        'pn': page,
    }
    url = 'http://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_java%E5%AE%9E%E4%B9%A0?city=%E5%B9%BF%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput=',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'user_trace_token=20180730235357-38cfec37-aff6-4c32-87ce-b77c54e69aef; _ga=GA1.2.726045596.1532966039; LGUID=20180730235359-c5bb10f6-9410-11e8-abdb-525400f775ce; LG_LOGIN_USER_ID=dda0beb818d88c0d97815ce07cd30ad9672d4758764d47fcc4ccf06565366daa; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=12; _gid=GA1.2.2126507714.1536652537; index_location_city=%E5%B9%BF%E5%B7%9E; JSESSIONID=ABAAABAAAIAACBIB7D396C61C0B4AD48AA3C76532ACCE66; LGSID=20180912151602-b49291e6-b65b-11e8-9591-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D-ZdDCipwaN8MhxIbZKQvER3OF7JBbMvCU87QhMyL-4i%26wd%3D%26eqid%3D9276e07d0003e483000000035b98bd2d; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1536652537,1536654630,1536678474,1536736562; _putrc=D8D16E6EA3B9CF48123F89F2B170EADC; login=true; unick=%E8%B0%AD%E6%9D%B0; gate_login_token=e3369ff4091ec4f478aae2234a8a586e7baf0cbb760c3249caf38b08d113f601; _gat=1; TG-TRACK-CODE=index_search; LGRID=20180912153224-fdcc29f3-b65d-11e8-b814-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1536737543; SEARCH_ID=89a30ecc441945b8b3266cd8a265ac13'
    }
    try:
        #r = requests.post(url, headers=headers, data=data, proxies=proxy, timeout=10)
        r = requests.post(url, headers=headers, data=data, timeout=10)
        if r.status_code == 200:
            print(r.json())
            return r.json()
        else:
            print('crawl page %s failed' % page)
    except Exception as e:
        print(e)
        return


def parse_jd_page(_id):
    url = 'https://www.lagou.com/jobs/%s.html' % _id
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.106 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers)
        html = r.text.replace('<br>', '')
        soup = BeautifulSoup(html, 'lxml')
        jd = soup.find('dd', class_='job_bt').get_text()
        addr = soup.find('dd', class_='job-address').get_text()
        addr = ''.join(addr.split())
        return jd, addr
    except Exception:
        return None, None


def parse_json(data):
    if data:
        try:
            results = data.get('content').get('positionResult').get('result')
            for result in results:
                lagou = {}
                #lagou['_id'] = results.ObjectId()
                lagou['postion_id'] = result.get('positionId')
                lagou['城市'] = result.get('city')
                lagou['公司名字'] = result.get('companyFullName')
                lagou['公司福利'] = result.get('companyLabelList')
                lagou['Logo'] = result.get('companyLogo')
                lagou['公司简称'] = result.get('companyShortName')
                lagou['公司大小'] = result.get('companySize')
                lagou['发布时间'] = result.get('createTime')
                lagou['区域'] = result.get('district')
                lagou['学历限制'] = result.get('education')
                lagou['融资'] = result.get('financeStage')
                lagou['职位类型'] = result.get('firstType')
                lagou['行业类型'] = result.get('industryField')
                lagou['职位'] = result.get('jobNature')
                lagou['职位优势'] = result.get('positionAdvantage')
                lagou['职位名'] = result.get('positionName')
                lagou['薪酬水平'] = result.get('salary')
                lagou['职位类别'] = result.get('secondType')
                lagou['地铁站'] = result.get('stationname')
                lagou['地铁线'] = result.get('subwayline')
                lagou['工作经验'] = result.get('workYear')
                yield lagou
        except ValueError as e:
            print(e)
            return
    else:
        return None


def save_to_mongo(data):
    if data:
        for d in data:
            job.insert(d)
            print('正在保存 %s 至mongodb'%d)
    else:
        return None


def main(keyword, page):
    data = get_json(keyword, page)
    parse_jd_page(data)
    data_gne = parse_json(data)
    save_to_mongo(data_gne)

if __name__ == '__main__':
    keyword = input('要爬取的职位:')
    pages = input('要爬取的页数:')
    job = db[keyword + '_threadings']

    t1 = time.time()

    threads = []
    for i in range(1, int(pages) + 1):
        t = threading.Thread(target=main, args=(keyword, i))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    t2 = time.time()

    print('多线线程版耗时%s秒' % (t2 - t1))