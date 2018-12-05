# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.files import FilesPipeline

from sharp_eye_spiders.items import PdfItem


class PdfPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['file_urls']:
            yield scrapy.Request(image_url, headers={'Referer': item['referer']})

    def item_completed(self, results, item, info):
        if not isinstance(item, PdfItem):
            return item
        print(results)
        for ok, result in results:
            if not ok:
                continue
        return super().item_completed(results, item, info)
