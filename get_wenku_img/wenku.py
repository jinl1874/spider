# 多线程爬取 轻小说文库的插图
# -*- coding:utf-8 -*-
import requests
import re
import os
import io
import sys
import threading
from lxml import etree
from queue import Queue

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def get_input():
    return input("输入插图链接:\n>>>")


class Wenku(threading.Thread):

    def __init__(self, name, queue, path_name):
        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue
        self.path_name = path_name

    def run(self):
        print(self.name + " start……")
        while not self.queue.empty():
            value = self.queue.get()
            save_img(value, path_name=self.path_name)
            print(self.name + ": " + value + "  download")
        print(self.name + " end……")


def parse_page(url: str):
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    html = etree.HTML(response.text)
    title = html.xpath("//div[@id='title']/text()")[0]
    image_links = html.xpath('//div[@id="content"]//a/@href')
    # for link in image_links:
    #     save_img(link, title)
    # mid = int(len(image_links)/2)
    # p1 = threading.Thread(target=save_img, args=(image_links[0:mid], title))
    # p2 = threading.Thread(target=save_img, args=(image_links[mid:], title))

    # p1.setDaemon(True)
    # p1.start()
    # p2.setDaemon(True)
    # p2.start()

    # p1.join()
    # p2.join()
    return image_links, title


def save_img(link, path_name):
    re_obj = re.match(r'.*?/pictures/\d+/\d+/\d+/(.*?jpg)', link)
    name = re_obj.group(1)
    r = requests.get(link, headers=headers)
    base_path = r'D://book//images'
    # 有中文名的话会出现乱码，所以需要重新解码编码
    file_path = os.path.join(base_path, path_name)
    file_path = base_path + '//' + path_name
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    file_path = os.path.join(file_path, name)
    with open(file_path, "wb+") as f:
        f.write(r.content)


def main():
    queue = Queue()
    url = "https://www.wenku8.net/novel/1/1546/74570.htm"
    urls, title = parse_page(url)
    for i in urls:
        queue.put(i)
    threads = []

    thread_list = ['thread-1', 'thread-2', 'thread-3']
    for i in thread_list:
        thread = Wenku(i, queue, title)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
