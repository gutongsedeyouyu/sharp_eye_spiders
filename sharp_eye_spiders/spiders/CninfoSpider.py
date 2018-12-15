import scrapy
from json import loads as json_loads

from sharp_eye_spiders.items import AnnouncementItem
from sharp_eye_spiders.models import _database, AnnouncementFile


class CninfoSpider(scrapy.Spider):
    name = "cninfo"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = _database

    def start_requests(self):
        yield scrapy.Request(url='http://www.cninfo.com.cn/new/disclosure?column=szse_latest&pageNum=1&pageSize=20', method='POST',
                             callback=self.parse, meta={'securityCodePrefix': 'SZ'})

    def parse(self, response):
        all_announcements = json_loads(response.body.decode('utf-8'))['classifiedAnnouncements']
        for announcements in all_announcements:
            for announcement in announcements:
                security_code = '{0}{1}'.format(response.meta['securityCodePrefix'], announcement['secCode'])
                file_url = 'http://www.cninfo.com.cn/{0}'.format(announcement['adjunctUrl'])
                if AnnouncementFile.exists(self.db, file_url):
                    return
                yield AnnouncementItem(security_code=security_code, company_name=announcement['secName'],
                                       title=announcement['announcementTitle'], announcement_time=announcement['announcementTime'],
                                       source='CNINFO', file_urls=[file_url], referer='')
