# 使用多线程爬取百度科幻小说吧前二十页的贴子
from queue import Queue
import requests
import re
from threading import Thread
from lxml import etree
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
}


# 创建生产者
class Producer(Thread):
    def __init__(self, base_queue: Queue, urls_queue: Queue):
        Thread.__init__(self)
        self.base_queue = base_queue
        self.urls_queue = urls_queue

    def run(self):
        while not self.base_queue.empty():
            url = self.base_queue.get()
            self.parse(url)

    def parse(self, url: str):
        res = requests.get(url, headers=headers)
        html = etree.HTML(res.text)
        urls = re.findall(r'<a rel="noreferrer" href="(/p/[0-9]+)"', res.text)
        # filter函数是将帖子地址筛选出来，而map函数是为了将地址与域名相结合
        alist = filter(lambda x: re.match(r"/p/[0-9]+", x), urls)
        alist = map(lambda x: 'https://tieba.baidu.com'+x, alist)
        # 将得到url入队
        for i in alist:
            self.urls_queue.put(i)


class Consumer(Thread):
    def __init__(self, base_queue: Queue, urls_queue: Queue):
        Thread.__init__(self)
        self.base_queue = base_queue
        self.urls_queue = urls_queue

    def run(self):
        time.sleep(3)
        # 如果两个队列都空了，那么就退出循环
        print(self.base_queue.empty(), self.urls_queue.empty())
        while not self.base_queue.empty() or not self.urls_queue.empty():
            url = self.urls_queue.get()

            self.save(url)

    def save(self, url):
        res = requests.get(url, headers=headers)
        html = etree.HTML(res.text)
        title = html.xpath(
            '//h3[contains(@class, "core_title_txt")]/@title')[0]
        author = html.xpath('//li[@class="d_name"]//text()')[1]
        time = html.xpath(
            '//div[@class="core_reply_tail clearfix"]//span/text()')[1]
        # 因为百度奇葩的代码，当有个性签名时，span标签会多一个
        if time in "1楼":
            time = html.xpath(
                '//div[@class="core_reply_tail clearfix"]//span/text()')[2]
        first_content = html.xpath(
            '//div[contains(@class, "l_post l_post_bright")][1]//cc/div[2]/text()')
        content = "\n".join(first_content)
        # 保存到一个markdown文件下
        with open('test.md', 'a', encoding='utf-8') as fp:
            text = '## {} \n > {} \n > {} \n {} \n\n'.format(
                title, author, time, content)
            print(text)
            fp.write(text)


def main():
    base_queue = Queue(20)
    urls_queue = Queue(1000)

    base_url = 'https://tieba.baidu.com/f?kw=%E7%A7%91%E5%B9%BB%E5%B0%8F%E8%AF%B4&ie=utf-8&pn={}'
    for i in range(20):
        url = base_url.format(i * 50)
        base_queue.put(url)

    for i in range(3):
        produce = Producer(base_queue, urls_queue)
        produce.start()

    for i in range(3):
        consum = Consumer(base_queue, urls_queue)
        consum.start()


if __name__ == '__main__':
    main()
