import scrapy
import os
import logging
from sina.items import SinaItem


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['sina.com.cn']
    start_urls = ['https://news.sina.com.cn/guide/']

    def parse(self, response):
        items = []
        base_path = 'J:\Desktop\sina'
        sub_links = response.xpath(
            "//div[@id='tab01']/div[@class='clearfix']//ul//a/@href").extract()
        sub_titles = response.xpath(
            "//div[@id='tab01']/div[@class='clearfix']//ul//a/text()").extract()
        parent_titles = response.xpath(
            "//div[@id='tab01']/div[@class='clearfix']//h3//text()").extract()
        parent_links = response.xpath(
            "//div[@id='tab01']/div[@class='clearfix']//h3//a/@href").extract()

        for i in range(len(parent_titles)-1):
            # 创建大类目录
            parent_path = os.path.join(base_path, parent_titles[i])
            if not os.path.exists(parent_path):
                os.mkdir(parent_path)

            for j in range(len(sub_titles)):
                item = SinaItem()
                item["parent_title"] = parent_titles[i]

                # 因为最后一个地方站没有url，所以得随加一个
                # if i == len(parent_links):
                #     item['parent_url'] = '*.sina.com.cn'
                # else:
                item['parent_url'] = parent_links[i]
                belong = sub_links[j].startswith(item["parent_url"])
                # 为了给地方站擦屁股
                # if i == len(parent_links) and j >= len(sub_titles) - 27:
                #     sub_path = os.path.join(parent_path, sub_titles[j])
                #     if not os.path.exists(sub_path):
                #         os.mkdir(sub_path)
                #     item['sub_url'] = sub_links[j]
                #     item['sub_title'] = sub_titles[j]
                #     item['sub_path'] = sub_path
                #     items.append(item)
                if belong:
                    sub_path = os.path.join(parent_path, sub_titles[j])
                    if not os.path.exists(sub_path):
                        os.mkdir(sub_path)
                    item['sub_url'] = sub_links[j]
                    item['sub_title'] = sub_titles[j]
                    item['sub_path'] = sub_path
                    items.append(item)

        # with open(r'J:\Desktop\test.txt', 'w') as fp:
        #     fp.write(i['sub_path'] + ' ' + i['sub_title'] +
        #                  ' ' + i['sub_url']+'\n')
        for i in items:
            yield scrapy.Request(url=i['sub_url'], callback=self.sub_parse, meta={'sub_item': i})

    def sub_parse(self, response):
        items = []
        urls = response.xpath("//a/@href").extract()
        # if()
        start_str = response.meta['sub_item']["sub_url"]
        start = start_str[0:4]+'s' + start_str[4:13]
        links = filter(lambda x: x.startswith(start)
                       and x.endswith("shtml"), urls)
        for link in links:
            item = {}
            item = response.meta['sub_item'].copy()
            item['url'] = link
            # items.append(item)
            # logging.warning(item['url'])
            yield scrapy.Request(url=item['url'], callback=self.grand_parse, meta={'item': item})

    def grand_parse(self, response):
        item = response.meta['item']
        title = response.xpath(
            "//h1[@class='main-title' or 'news-title']/text()").extract()
        # date = response.xpath("//span[@class='date']/text()").extract()[0]
        date = response.xpath(
            "//span[@class='date']/text()|//div[@class='wz-tbbox']/span[@class='wz-fbtime']/text()").extract()
        if title and date:
            item['title'] = title[0]
            item['date'] = date[0]
            content = response.xpath(
                "//div[@class='article']//text()").extract()
            if not content:
                content = response.xpath(
                    "//div[@class='textbox']//text()").extract()
            content_str = "\n".join(content)
            item['content'] = content_str
            logging.warning(item['title'])
            yield item
