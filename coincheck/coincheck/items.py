# -*- coding: utf-8 -*-
import scrapy


class TickerItem(scrapy.Item):
    # define the fields for your item here like:
    market_id = scrapy.Field()
    bid = scrapy.Field()
    ask = scrapy.Field()
    volume = scrapy.Field()
    status = scrapy.Field()
    created_at = scrapy.Field()

