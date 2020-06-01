# 下载芝士漫画里的章节，找到该漫画的某一章节章节链接，可自动选择下一章漫画或者下载新的url
import requests
import sys
import io
import os
import re
import time
from lxml import etree
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfgen import canvas


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"
}

# 默认url
url = "https://manhua.zsh8.com/pxtt/pxtt-040/91864.html"

# 解析出url中的章节名
re_object = re.match(
    "https://manhua.zsh8.com/.*?/(.*?)/.*?html", url)
chapter = re_object.group(1)

# 当前目录
current_dir = os.getcwd()


# 得到返回文件
def get_text(url):
    response = requests.get(url, headers=headers)
    return response


# 分析文档
def parse_text(text):
    # 建立解析
    html = etree.HTML(text, etree.HTMLParser())
    # 获取下一章节的links
    links = html.xpath("//div[@id='gallery-1']//dt/a/@href")
    # 获取class="gallery-1"的div标签下的dt标签，再获取链接。
    dts = html.xpath("//dt[@class='gallery-icon portrait']")
    for i, link in enumerate(links):
        save_image(link, i)
        # 降低访问的速度，防止被识别为机器人
        time.sleep(15)
        print("完成", i, "个......")
    print("已完成", chapter, "的下载!")

    #　在第一章的时候只有一个next_chapter链接
    try:
        next_chapter = html.xpath(
            "//div[@class='fusion-single-navigation-wrapper']/a/@href")[1]
    except Exception as e:
        next_chapter = html.xpath(
            "//div[@class='fusion-single-navigation-wrapper']/a/@href")[0]
        return next_chapter
    return next_chapter


# 保存图片
def save_image(link, index):
    read = requests.get(link)
    dir_ = current_dir + '\\' + chapter
    if not os.path.exists(dir_):
        os.makedirs(dir_)
    with open(dir_ + '\\{}'.format(str(index)+".jpg"), 'wb') as fp:
        fp.write(read.content)
        fp.close()


# 保存为pdf
def convert_images_to_pdf(img_path, pdf_path):
    pages = 0
    (w, h) = portrait(A4)
    c = canvas.Canvas(pdf_path, pagesize=portrait(A4))
    l = os.listdir(img_path)
    l.sort(key=lambda x: int(x[:-4]))
    for i in l:
        f = img_path + os.sep + str(i)
        c.drawImage(f, 0, 0, w, h)
        c.showPage()
        pages = pages + 1
    c.save()


# 开始
def begin():
    global url
    global re_object
    global chapter
    local_url = input(
        "输入要下载的章节url(例: https://manhua.zsh8.com/pxtt/pxtt-041/93181.html)\n>>>")
    # 判断是否符合url格式
    re_object = re.match(
        "https://manhua.zsh8.com/.*?/(.*?)/.*?html", local_url)
    if (re_object):
        url = local_url
        re_object = re.match(
            "https://manhua.zsh8.com/.*?/(.*?)/.*?html", url)
        chapter = re_object.group(1)
        print("即将开始.....")
    else:
        print("输入错误！将使用默认链接！\n")


if __name__ == "__main__":
    begin()
    boolean = "y"
    count = 0
    if not os.path.exists(current_dir + '\\pdf\\'):
        os.makedirs(current_dir + '\\pdf\\')
    while(boolean == "y"):
        text = get_text(url).text
        next_chapter = parse_text(text)

        img_path = current_dir + '\\' + chapter
        pdf_path = current_dir + '\\pdf\\' + chapter + '.pdf'
        #　有些图片是错误，会导致无法生成pdf文件。
        try:
            convert_images_to_pdf(img_path, pdf_path)
        except Exception as e:
            print(e)
        re_object = re.match(
            "https://manhua.zsh8.com/.*?/(.*?)/.*?html", next_chapter)
        chapter = re_object.group(1)
        print("下一章节：", chapter)
        count += 1
        print(count)
        #　下载章节的数目
        if (count > 37):
            break
        url = next_chapter
