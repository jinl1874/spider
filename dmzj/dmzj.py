import os
import time
from random import uniform

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By


def getMainPage(url: str):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except:
        print(response.status_code)


def getChapters(html):
    html = etree.HTML(html)
    chapters = html.xpath(
        "//div[contains(@class, 'tab-content zj_list')]/ul[contains(@class, 'list_con_li autoHeight')]/li/a/@href")
    return chapters


def getImage(pages):
    browser = webdriver.Chrome()
    for page in pages:
        browser.get(str(page))
        page_num = browser.find_elements_by_xpath(
            "//div[@class='btmBtnBox']/select[@id='page_select']/option")
        for num in range(1, len(page_num)+1):
            image_page = str(page) + "#page={num}".format(num=num)
            browser.get(image_page)
            image_url = browser.find_element_by_xpath(
                "//div[contains(@class, 'comic_wraCon autoHeigh')]/img")
            book_title = browser.find_element_by_xpath(
                "//div[@class='head_title']/h1/a")
            chapter_title = browser.find_element_by_xpath(
                "//div[@class='head_title']/h2")

            image_url = image_url.get_attribute('src')
            book_title = book_title.text
            chapter_title = chapter_title.text
            # 设置随机访问时间
            t = uniform(0, 10)
            print(t)
            time.sleep(t)

            yield image_url, book_title, chapter_title, num, page

    browser.close()


def saveImage(image):
    for im, name, title, page, referer_page in image:
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'referer': referer_page,
        }

        image_response = requests.get(im, headers=headers)
        if not os.path.exists(u'E:\dmzj\{name}'.format(name=name)):
            os.mkdir(u'E:\dmzj\{name}'.format(name=name))

        if not os.path.exists(u'E:\dmzj\{name}\{title}'.format(name=name, title=title)):
            os.mkdir(u'E:\dmzj\{name}\{title}'.format(name=name, title=title))

        if image_response.status_code == 200:
            file_path = u'E:\dmzj\{name}\{title}\{page}.jpg'.format(
                name=name, title=title, page=page)

        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(image_response.content)
        else:
            print(image_response.status_code)


def main():
    url = 'https://www.dmzj.com/info/jinglingzhidan.html'
    html = getMainPage(url)
    pages = getChapters(html)
    image = getImage(pages)
    saveImage(image)


if __name__ == '__main__':
    main()
