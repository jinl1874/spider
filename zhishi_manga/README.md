### 写代码

1. 新建一个 python 文件
2. 导入相应的模块

```
import requests
import sys
import io
import os
import re
import time
from lxml import etree
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfgen import canvas
```

3. 定义全局变量

```
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"
}

# 默认url
url = "https://manhua.zsh8.com/pxtt/pxtt-040/91864.html"

# 解析出url中的章节名
re_object = re.match(
    "https://manhua.zsh8.com/.*?/(.*?)/.*?html", url)
chapter = re_object.group(1)

# 文件当前目录
current_dir = os.getcwd()
```

4. 定义方法

   - get_text()：得到访问返回的资源

   ```
   def get_text(url):
       response = requests.get(url, headers=headers)
       return response
   ```

   - parse_text(text)：分析文档，保存图片，并得到下一章的 url

   ```
   def parse_text(text):
       # 建立解析
       html = etree.HTML(text, etree.HTMLParser())
       # 获取漫画图片所有的链接
       links = html.xpath("//div[@id='gallery-1']//dt/a/@href")
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

   ```

   - save_image(link, index): 访问得到的图片链接，并保存在本地

   ```
   def save_image(link, index):
       read = requests.get(link)
       # 当前文件夹的加上章节名形成新的文件夹
       dir_ = current_dir + '\\' + chapter
       # 创建文件夹
       if not os.path.exists(dir_):
           os.makedirs(dir_)
       # 保存图片
       with open(dir_ + '\\{}'.format(str(index)+".jpg"), 'wb') as fp:
           fp.write(read.content)
           fp.close()
   ```

   - convert_images_to_pdf(img_path, pdf_path)：根据图片的文件夹以及 pdf 文件夹加上文件名来生成 pdf 文件

   ```
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
   ```

   - begin()：开始，并更新全局变量名

   ```
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
           # 更新章节名
           re_object = re.match(
               "https://manhua.zsh8.com/.*?/(.*?)/.*?html", url)
           chapter = re_object.group(1)
           print("即将开始.....")
       else:
           print("输入错误！将使用默认链接！\n")

   ```

   - main()：主函数

   ```
   if __name__ == "__main__":
       begin()
       boolean = "y"
       count = 0
       # 保存pdf的文件夹
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
           #　下载章节的数目，可根据自己需要更改
           if (count > 37):
               break
           url = next_chapter
   ```

### 运行

直接在终端运行 python 文件，等待一段时间，就会在 python 文件的当前目录下生成文件。
![文件夹](http://image.jinl1874.xyz/img/20200615222857.png)
文件夹里的图片：
![图片](http://image.jinl1874.xyz/img/20200615222947.png)
pdf 文件：
![pdf](http://image.jinl1874.xyz/img/20200615223024.png)

完整代码可参考我的[github 库](https://github.com/jinl1874/spider)