import os
import json
import logging
import scrapy

from datetime import datetime
from coincheck.items import TickerItem
from scrapy.utils.log import configure_logging

logger = logging.getLogger('coincheck')


class CoincheckSpider(scrapy.Spider):
    name = 'coincheck'
    allowed_domains = ["coincheck.com"]
    ticker_url = 'https://coincheck.com/api/ticker'
    start_urls = [ticker_url]
    download_delay = 20

    def __init__(self, name=None, **kwargs):
        # set logging
        logger.setLevel(logging.INFO)
        ch = logging.FileHandler('coincheck.log', mode='a')
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        super(CoincheckSpider, self).__init__(name, **kwargs)
        self.info('CoincheckSpider started')
        self.info('=======================')

    def info(self, message):
        self.log(message, level=logging.INFO)

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        posix_time = jsonresponse["timestamp"]
        dt = datetime.utcfromtimestamp(posix_time).strftime('%Y-%m-%dT%H:%M:%S')
        item = TickerItem()
        item["market_id"] = 1
        item["bid"] = jsonresponse["bid"]
        item["ask"] = jsonresponse["ask"]
        item["volume"] = jsonresponse["volume"]
        item["status"] = 0
        item["created_at"] = dt

        self.info('created_at: %s' % item["created_at"])
        yield item
        yield scrapy.Request(self.ticker_url, callback=self.parse, dont_filter=True)
