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
        yield scrapy.Request(url='http://www.cninfo.com.cn/new/index/getAnnouces?type=sz', callback=self.parse)

    def parse(self, response):
        all_announcements = json_loads(response.body.decode('utf-8'))['classifiedAnnouncements']
        for announcements in all_announcements:
            for announcement in announcements:
                if AnnouncementFile.exists(self.db, announcement['adjunctUrl']):
                    return
                yield AnnouncementItem(security_code=announcement['secCode'], company_name=announcement['secName'],
                                       title=announcement['announcementTitle'], announcement_time=announcement['announcementTime'],
                                       file_urls=['http://www.cninfo.com.cn/{0}'.format(announcement['adjunctUrl'])],
                                       referer='')
