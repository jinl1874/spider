# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 父类标题
    parent_title = scrapy.Field()
    parent_url = scrapy.Field()
    # 子类标题
    sub_title = scrapy.Field()
    sub_url = scrapy.Field()
    sub_path = scrapy.Field()

    # 标题
    url = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    # 内容
    content = scrapy.Field()
