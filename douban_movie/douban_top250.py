# 爬取豆瓣网top250电影
import re
import csv
import requests
import itertools
movies = []


def parse_der_act_time_s(list_der):
    new_list = []
    for der in list_der:
        new_list.append(re.sub(r'<.*?>|&nbsp;|\s{2,20}', '', der))
    return new_list


def parse_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    # proxy = {
    #     'HTTPS': '171.113.156.73:8010'
    # }
    response = requests.get(url, headers=headers)
    text = response.text
    titles = re.findall(
        r'<a.*?<span class="title">(.*?)</span>', text, re.DOTALL)
    scores = re.findall(
        r'<span class="rating_num".*?>(.*?)</span>', text, re.DOTALL)
    comment_nums = re.findall(
        r'<span class="rating_num".*?>.*?<span>(.*?)</span>', text, re.DOTALL)
    der_act_time_s = re.findall(
        r'<div class="bd">.*?<p.*?(导.*?)</p>', text, re.DOTALL)
    movie_peoples = parse_der_act_time_s(der_act_time_s)
    short_comments = re.findall(
        r'<p class="quote">.*?<span class="inq">(.*?)</span>', text, re.DOTALL)
    # 将数据保存到一个列表中
    for value in zip(titles, scores, comment_nums, movie_peoples, short_comments):
        title, score, comment_num, movie_information, short_comment = value
        movie = {
            'title': title,
            'score': score,
            'comment_num': comment_num,
            'movie_information': movie_information,
            'short_comment': short_comment
        }
        movies.append(movie)


def write_csv():
    header = ['title', 'score', 'comment_num',
              'movie_information', 'short_comment']
    # 写入一个 csv文件里
    with open('豆瓣TOP250电影.csv', 'w', encoding='utf-8', newline='') as fp:
        writer = csv.DictWriter(fp, header)
        writer.writeheader()
        writer.writerows(movies)


def main():
    loop_25 = itertools.takewhile(lambda x: x <= 225, itertools.count(0, 25))
    for i in loop_25:
        incomplete_url = 'https://movie.douban.com/top250?start={}&filter='.format(
            i)
        parse_page(incomplete_url)
    write_csv()


if __name__ == '__main__':

    main()
