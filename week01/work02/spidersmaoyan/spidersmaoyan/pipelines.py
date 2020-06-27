# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SpidersmaoyanPipeline:
    def process_item(self, item, spider):
        filmtitle=item['filmtitle']
        filmtype=item['filmtype']
        filmdate=item['filmdate']
        output = f'|{filmtitle}|\t|{filmtype}|\t|{filmdate}|\n\n'
        with open('./maoyanmovie.txt', 'a+', encoding='utf-8') as article:
            article.write(output)

        return item
