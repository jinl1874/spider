import requests
import json
import math
import codecs
import csv

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'WM_TID=36fj4OhQ7NdU9DhsEbdKFbVmy9tNk1KM; _iuqxldmzr_=32; _ntes_nnid=26fc3120577a92f179a3743269d8d0d9,1536048184013; _ntes_nuid=26fc3120577a92f179a3743269d8d0d9; __utmc=94650624; __utmz=94650624.1536199016.26.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); WM_NI=2Uy%2FbtqzhAuF6WR544z5u96yPa%2BfNHlrtTBCGhkg7oAHeZje7SJiXAoA5YNCbyP6gcJ5NYTs5IAJHQBjiFt561sfsS5Xg%2BvZx1OW9mPzJ49pU7Voono9gXq9H0RpP5HTclE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed5cb8085b2ab83ee7b87ac8c87cb60f78da2dac5439b9ca4b1d621f3e900b4b82af0fea7c3b92af28bb7d0e180b3a6a8a2f84ef6899ed6b740baebbbdab57394bfe587cd44b0aebcb5c14985b8a588b6658398abbbe96ff58d868adb4bad9ffbbacd49a2a7a0d7e6698aeb82bad779f7978fabcb5b82b6a7a7f73ff6efbd87f259f788a9ccf552bcef81b8bc6794a686d5bc7c97e99a90ee66ade7a9b9f4338cf09e91d33f8c8cad8dc837e2a3; JSESSIONID-WYYY=G%5CSvabx1X1F0JTg8HK5Z%2BIATVQdgwh77oo%2BDOXuG2CpwvoKPnNTKOGH91AkCHVdm0t6XKQEEnAFP%2BQ35cF49Y%2BAviwQKVN04%2B6ZbeKc2tNOeeC5vfTZ4Cme%2BwZVk7zGkwHJbfjgp1J9Y30o1fMKHOE5rxyhwQw%2B%5CDH6Md%5CpJZAAh2xkZ%3A1536204296617; __utma=94650624.1052021654.1536048185.1536199016.1536203113.27; __utmb=94650624.12.10.1536203113',
    'Host': 'music.163.com',
    'Referer': 'http://music.163.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
}


comments = []


def get_comment(url, data, song_name):
    r = requests.post(url, headers=headers, data=data)
    text = json.loads(r.text)
    for i in text['data']['hotComments']:
        comment = {}
        comment['name'] = i['user']['nickname']
        comment['content'] = i['content']
        comment['votes'] = i['likedCount']
        print(comment)
        comments.append(comment)


def save(comments):
    headers = ['name', 'content', 'votes']
    with open('test.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerows(comments)


def main():
    song_name = '富士山下'
    song_id = '65766'
    page = 1
    url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
    # 根据抓包找到相对应的值
    payload = {
        "params": "orqzo+bzkNn3k8Z3Gxw96dwTOiasvUUUq1y0UPvyhjq+hw2NMPWGTo1N7bN+x85I3HltI7vtlZ/sh/s5x8hStUUYNE7bUztMuW+Jjxvm6DP01bGmJxOdJFM91psiJKURZ5afHS5W/k1E6dpMR7u9S8+05ELx5p3hFgGRjQG4qGimkdSnbyQnHzzy8LIKx0yIe8DpqLscVVrveJu0m7qjti4+P6cNNz+V/cM0nIcfRSyQ+vJHVgVVTPsc2I8El3VrTJgZWFD3gF3Mc1tpljKvCw==",
        "encSecKey": "92f608177401135e7f170add75730355ed8dbbe3c0a16dde1882bba747b2e5a8de2860ba0bcb93d27112a65e52d0088b46e529fab7ae792f750f8c57dbd3230db2ba341601338093b43831874f6508c5f3b56d48c2e913876c6d86e1ad0e705f7b7e4804d128087240f941103d0088714844b099bf6167a9d7f4f95055e1c4d6"
    }
    get_comment(url, payload, song_name)
    save(comments)


if __name__ == "__main__":
    main()
