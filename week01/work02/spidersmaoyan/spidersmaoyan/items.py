# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpidersmaoyanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    filmtitle = scrapy.Field()
    filmtype = scrapy.Field()
    filmdate = scrapy.Field()
