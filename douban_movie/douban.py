import requests
from lxml import etree
from datetime import datetime

# 获取豆瓣电影页面
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
    "Referer": 'https://movie.douban.com/'
}
# 地区可更换
url = 'https://movie.douban.com/cinema/nowplaying/guangzhou/'
response = requests.get(url, headers=headers)

# 提取数据
html = etree.HTML(response.text)
ul = html.xpath('//ul[@class="lists"]')[0]
lis = ul.xpath('./li')
# 获取当前时间
now_time = datetime.now()
# 为文件命名
file_name = ('上映电影(%d.%d.%d).txt' %
             (now_time.year, now_time.month, now_time.day))
with open(file_name, 'w') as fb:
    fb.truncate()
for li in lis:
    title = li.xpath('@data-title')[0]
    score = li.xpath('@data-score')[0]
    began_time = li.xpath('@data-release')[0]
    duration = li.xpath('@data-duration')[0]
    region = li.xpath('@data-region')[0]
    director = li.xpath('@data-director')[0]
    actors = li.xpath('@data-actors')[0]
    text = ('%s  %s\n\t豆瓣评分：%s\n\t时长：%s  \n\t地区：%s\n\t导演：%s\n\t主演：%s\n\n\n' %
            (title, began_time, score, duration, region, director, actors))
    with open(file_name, 'a', encoding='utf-8') as fb:
        fb.write(text)
