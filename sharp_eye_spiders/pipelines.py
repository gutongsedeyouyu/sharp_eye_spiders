# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime

import scrapy
from scrapy.pipelines.files import FilesPipeline

from sharp_eye_spiders.items import AnnouncementItem
from sharp_eye_spiders.models import _database, AnnouncementFile


class AnnouncementPipeline(FilesPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = _database

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url, headers={'Referer': item['referer']})

    def item_completed(self, results, item, info):
        if not isinstance(item, AnnouncementItem):
            return item
        for ok, result in results:
            if not ok:
                continue
            AnnouncementFile.add(self.db, security_code=item['security_code'], company_name=item['company_name'],
                                 title=item['title'],
                                 announcement_time=datetime.fromtimestamp(int(item['announcement_time']) / 1000),
                                 file_url=result['url'], original_url=result['url'])
        return super().item_completed(results, item, info)
