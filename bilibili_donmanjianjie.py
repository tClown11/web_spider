import requests
import re
import json
'''
    对bilibilli的连载日本动画进行信息爬取，
    '''



class Video(object):
    def __init__(self,name,see,intro):
        self.name=name
        self.see=see
        self.intro=intro

    def __str__(self):
        return '''
        名称:{}
        播放量:{}
        简介:{}
        '''.format(self.name,self.see,self.intro)

class bilibili:
    recent_url = "https://bangumi.bilibili.com/api/timeline_v2_global"  # 最近更新
    detail_url = "https://bangumi.bilibili.com/anime/{season_id}"

    def __init__(self):
        self.dom = requests.get('https://www.bilibili.com').text


    def get_recent(self):
        items = json.loads(requests.get(self.recent_url).text)['result']
        #print(items)
        videos = []
        for i in items:
            #使用bilibili后台提供的api接口获取番剧的基本数据
            link = self.detail_url.format(season_id=i['season_id'])
            d = requests.get(url=link).text#拼接url

            '''
                用正则表达式，匹配出番剧名称，播放量，追番人数，弹幕总数，还有番剧的简介
            '''

            name = re.findall('name="keywords" content="(.*?)"', d, re.S)
            see = re.findall('class="media-info-label">(.*?)</span><em>(.*?)</em', d, re.S)
            intro = re.findall('name="description" content="(.*?)"', d, re.S)
            intro = re.sub('\n', '', intro[0])

            #将数据按照一定的格式保存
            r = Video(name=name[0], intro=intro, see=see)
            videos.append(r)
        for i in videos:
            print(i)
            pass



if __name__ == "__main__":
    r = bilibili()
    r.get_recent()