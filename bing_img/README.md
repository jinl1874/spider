### 编码
1. 导入模块和设置变量
```python
import re
import os
import requests
from lxml import etree
import io
import sys


url = 'https://cn.bing.com/'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537."
    "36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}
```

2. 使用requests库请求必应首页的资源
```python
response = requests.get(url, headers=headers)
```
3. 使用xpath解析出图片的名字与链接
```python
# 使用xpath解析得到数据
html = etree.HTML(response.text, etree.HTMLParser())
# 得到图片链接
image_url = html.xpath("//head//link[@id='bgLink']/@href")[0]
# 得到一个名字与版权的字符串
filename = html.xpath("//a[@id='sh_cp']/@title")[0]
# 使用正则表达式去除版权商
re_object = re.match('(.*?)\s.*?\\)', filename)
filename = re_object[1]
# 因为得到 image_url 是没网址前缀的，所以需要加上
pic_url = url + image_url
filename = filename + ".jpg"
```

4. 生成一个文件夹放置图片
```python
# 当前的文件目录
current_dir = os.getcwd()
img_dir = current_dir + "\\bing_img"
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
```
5. 保存图片
```python
read = requests.get(pic_url)
# 保存图片
with open(img_dir + '\\{}'.format(filename), 'wb') as fp:
    fp.write(read.content)
    fp.close()
```

### 运行

在命令行下运行该文件，会得到一个文件夹，图片就放在里面。


[github地址](https://github.com/jinl1874/spider)
