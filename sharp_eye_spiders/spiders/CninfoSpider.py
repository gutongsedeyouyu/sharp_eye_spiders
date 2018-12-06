import scrapy
from json import loads as json_loads

from sharp_eye_spiders.items import AnnouncementItem


class CninfoSpider(scrapy.Spider):
    name = "cninfo"

    def start_requests(self):
        yield scrapy.Request(url='http://www.cninfo.com.cn/new/index/getAnnouces?type=sz', callback=self.parse)

    def parse(self, response):
        all_announcements = json_loads(response.body.decode('utf-8'))['classifiedAnnouncements']
        for announcements in all_announcements:
            yield AnnouncementItem(security_code=announcements[0]['secCode'], company_name=announcements[0]['secName'],
                                   title=announcements[0]['announcementTitle'], announcement_time=announcements[0]['announcementTime'],
                                   file_urls=['http://www.cninfo.com.cn/{0}'.format(a['adjunctUrl']) for a in announcements],
                                   referer='')
