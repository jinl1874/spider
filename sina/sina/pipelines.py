# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os


class SinaPipeline:
    def process_item(self, item, spider):
        base_path = item['sub_path']
        file_path = os.path.join(base_path, item['title'] + '.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('## ' + item['title'] + '\n\n')
            f.write('> 时间：'+item['date'] + '\n\n')
            f.write(item['content'])
        return item
