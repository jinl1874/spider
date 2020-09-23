## Scrapy 爬取 Django 的官方中文文档

### 起因

因为最近刚学了点 scrapy 和 django，就用 scrapy 来练练手。

### 准备

安装 scrapy

```shell
pip install scrapy
```

当输入 scrapy 出现以下字段时，说明安装成功了：

```shell
Scrapy 2.3.0 - no active project

Usage:
  scrapy <command> [options] [args]

Available commands:
  bench         Run quick benchmark test
  commands
  fetch         Fetch a URL using the Scrapy downloader
  genspider     Generate new spider using pre-defined templates
  runspider     Run a self-contained spider (without creating a project)
  settings      Get settings values
  shell         Interactive scraping console
  startproject  Create new project
  version       Print Scrapy version
  view          Open URL in browser, as seen by Scrapy

  [ more ]      More commands available when run from project directory

Use "scrapy <command> -h" to see more info about a command
```

安装 xpath 依赖

```shell
pip install lxml
```



### 思路

打开所要爬取的的索引文档  https://docs.djangoproject.com/zh-hans/3.0/intro/ ，然后提取相对应的的链接到一个列表中。最后遍历整个列表，提取相对应的文本，再使用正则表达式，将 html 文本替换成 markdown 文本，保存相应的地方。



### 使用

在 `/spider/document.py parse_pag()` 设置下载后的文件夹的位置：

```python
	# 放置文档的地方，可更改 
    base_path = r'D:\web\django-doc'
```

然后使用 PowerShell 进入scrapy的最高目录，输入`scrapy crawl django-doc`并回车。

最后会在相对应的文件夹下生成 Markdown 文件

![image-20200923120909368](http://image.jinl1874.xyz/img/image-20200923120909368.png)

实际对比

官方文档：

![image-20200923121136682](http://image.jinl1874.xyz/img/image-20200923121136682.png)



Markdown：

![image-20200923121214190](http://image.jinl1874.xyz/img/image-20200923121214190.png)

> 图片来自 markdown 编辑器 typora



### 爬取其它目录

将 `spider/document.py start_request()` 里的 urls 链接改为其它，比如 https://docs.djangoproject.com/zh-hans/3.0/topics/ ，然后再将 `replace()`的

```python 
sub_text = re.sub(r'\.\./', r'https://docs.djangoproject.com/zh-hans/3.0/intro', sub_text)
```

改为：

```python
sub_text = re.sub(r'\.\./', r'https://docs.djangoproject.com/zh-hans/3.0/topics', sub_text)
```

也就是说，要爬取哪个目录，就要将相对应的目录链接改名。