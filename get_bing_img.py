# -*-coding:utf-8-*
# 获取bing首页的图片
import re
import os
import requests
from lxml import etree
import io
import sys
import chardet

url = 'https://cn.bing.com/'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537."
    "36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}

# 防止打印时出现编码错误
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

response = requests.get(url, headers=headers)
count = 1
html = etree.HTML(response.text, etree.HTMLParser())
# 得到图片链接
image_url = html.xpath("//head//link[@id='bgLink']/@href")[0]
filename = html.xpath("//a[@id='sh_cp']/@title")[0]
# 解析出图片名字
re_object = re.match('(.*?)\s.*?\\)', filename)
filename = re_object[1]
pic_url = url + image_url
filename = filename + ".jpg"


read = requests.get(pic_url)
current_dir = os.getcwd()
img_dir = current_dir + "\\bing_img"
if not os.path.exists(img_dir):
    os.makedirs(img_dir)

# 保存图片
with open(img_dir + '\\{}'.format(filename), 'wb') as fp:
    fp.write(read.content)
    fp.close()
