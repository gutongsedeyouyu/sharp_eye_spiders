# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnnouncementItem(scrapy.Item):
    security_code = scrapy.Field()
    company_name = scrapy.Field()
    title = scrapy.Field()
    announcement_time = scrapy.Field()
    source = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    referer = scrapy.Field()
