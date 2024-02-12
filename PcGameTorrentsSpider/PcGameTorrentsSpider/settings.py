# Scrapy settings for PcGameTorrentsSpider project

BOT_NAME = "PcGameTorrentsSpider"

SPIDER_MODULES = ["PcGameTorrentsSpider.spiders"]
NEWSPIDER_MODULE = "PcGameTorrentsSpider.spiders"

# Pretend to be a real browser to avoid anti-scraping measures
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/90.0.4430.212 Safari/537.36")

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 1  # A delay of 1s between requests to avoid getting banned
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Configure item pipelines
ITEM_PIPELINES = {
    'PcGameTorrentsSpider.pipelines.PcgametorrentsspiderPipeline': 300,
}

# Enable and configure AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
