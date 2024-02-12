import scrapy
from ..items import GameItem
from scrapy import signals
from dataclasses import dataclass


@dataclass
class Game:
    name: str = None
    post_date: str = None
    info: str = None
    link: str = None


class PcGameTorrentsSpider(scrapy.Spider):
    name = 'PcGameTorrents_Spider'
    allowed_domains = ['pcgametorrents.com']


    def __init__(self, game_name=None, *args, **kwargs):
        super(PcGameTorrentsSpider, self).__init__(*args, **kwargs)
        self.game_name = game_name
        self.url = "https://pcgametorrents.com/"
        self.games = []


    def start_requests(self):
        if self.game_name:
            url = f'{self.url}?s={self.game_name.replace(" ", "+")}'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for game_li in response.xpath('//div[@class="uk-first-column"]'):
            item = GameItem()
            item['name'] = game_li.xpath('.//h2[@class="uk-article-title"]/a/text()').get()
            item['post_date'] = game_li.xpath('.//time/@datetime')
            item['info'] = game_li.xpath('.//div[@class="uk-margin-medium"]/p/text()')
            item['link'] = response.urljoin(game_li.xpath('.//h2[@class="uk-article"]/a/@href'))

            self.games.append(Game(item['name'], item['post_date'], item['info'], item['link']))
            yield item

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(PcGameTorrentsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, reason):
        if reason == 'finished':
            for i, game in enumerate(self.games):
                print(f'{i + 1}: Name: {game.name}\nPost Date: {game.post_date}\nInfo: {game.info}\nLink: {game.link}')
        else:
            print("The spider was closed due to an error.")
