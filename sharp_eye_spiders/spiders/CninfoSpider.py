import scrapy
from json import loads as json_loads

from sharp_eye_spiders.items import PdfItem


class CninfoSpider(scrapy.Spider):
    name = "cninfo"

    def start_requests(self):
        yield scrapy.Request(url='http://www.cninfo.com.cn/new/index/getAnnouces?type=sz', callback=self.parse)

    def parse(self, response):
        all_announcements = json_loads(response.body.decode('utf-8'))['classifiedAnnouncements']
        for announcements in all_announcements:
            yield PdfItem(company_name=announcements[0]['secName'], title=announcements[0]['announcementTitle'],
                          file_urls=['http://www.cninfo.com.cn/{0}'.format(a['adjunctUrl']) for a in announcements],
                          referer='')
