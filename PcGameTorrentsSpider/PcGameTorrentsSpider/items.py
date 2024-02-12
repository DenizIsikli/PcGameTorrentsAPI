import scrapy


class GameItem(scrapy.Item):
    name = scrapy.Field()
    info = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
