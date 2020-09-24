import os
import re

import scrapy


class DocumentDownload(scrapy.Spider):
    name = 'django-doc'

    def start_requests(self):
        urls = [
            'https://docs.djangoproject.com/zh-hans/3.0/intro/',
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # 获取所有章节标签
        a_tags = response.xpath(
            ".//div[@class='toctree-wrapper compound']//li/a")
        # 所有的章节名
        chapter_names = a_tags.xpath("text()").getall()
        # 所有的章节 url
        links = a_tags.xpath("@href").getall()

        # for (link, name) in zip(links, chapter_names):
        for i in range(len(links)):
            link = response.urljoin(links[i])
            yield scrapy.Request(link, callback=self.parse_page, meta={'name': str(i) + '. ' + chapter_names[i], })

    def parse_page(self, response):
        # 获取该链接的文本
        text = response.xpath("//div[@id='docs-content']/div").getall()[0]
        text = self.replace(text)

        # 放置文档的地方，可更改
        base_path = r'D:\web\django-doc'
        if not os.path.exists(base_path):
            os.mkdir(base_path)
        file_name = os.path.join(base_path, response.meta['name']+'.md')
        # 将其写入文件里
        with open(file_name, 'w', encoding='utf-8') as fp:
            fp.write(text)

    # 将得到的html代码转为 markdown 文本
    def replace(self, text: str) -> str:
        sub_text = re.sub(r'<h1>(.*?)</h1>', r'# \1', text)
        sub_text = re.sub(r'<h2>(.*?)</h2>', r'## \1', sub_text)
        sub_text = re.sub(r'<h3>(.*?)</h3>', r'### \1', sub_text)
        sub_text = re.sub(r'<h4>(.*?)</h4>', r'#### \1', sub_text)
        sub_text = re.sub(r'<a.*?href="(.*?)".*?>(.*?)</a>',
                          r'[\2](\1)', sub_text)
        sub_text = re.sub(
            r'\.\./\.\./', r'https://docs.djangoproject.com/zh-hans/3.0/', sub_text)
        sub_text = re.sub(
            r'\.\./', r'https://docs.djangoproject.com/zh-hans/3.0/intro/', sub_text)
        sub_text = re.sub(r'\[(.*?)\]\(#.*?\)', r'\1', sub_text)
        sub_text = re.sub(r'<pre.*?>', r'```python\n', sub_text)
        sub_text = re.sub(r'</pre>', r'```', sub_text)
        sub_text = re.sub(r'<strong>(.*?)</strong>', r'--\1--', sub_text)
        sub_text = re.sub(
            r'<div.*?>|<p.*?>|<section.*?>|<span.*?>|<ul.*?>|<li.*?>|<input.*?>|<label.*?>|<label.*?>|</label>|</section>|</span>|</div>|</ul>|</li>|</p>', '', sub_text)
        sub_text = re.sub(r'<em>(.*?)</em>', r'_\1_', sub_text)
        sub_text = re.sub(r'<code.*?>(.*?)</code>', r'`\1`', sub_text)

        sub_text = sub_text.replace("&gt;", ">")
        sub_text = sub_text.replace("&lt;", "<")
        return sub_text
