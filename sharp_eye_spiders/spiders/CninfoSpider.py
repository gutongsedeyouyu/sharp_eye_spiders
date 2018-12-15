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
        yield scrapy.Request(url='http://www.cninfo.com.cn/new/index/getAnnouces?type=sz',
                             callback=self.parse_page_count, meta={'securityCodePrefix': 'SZ'})

    def parse_page_count(self, response):
        security_code_prefix = response.meta['securityCodePrefix']
        page_num = 1
        page_count = int(json_loads(response.body.decode('utf-8'))['totalpages'])
        yield scrapy.Request(url=self.page_url(security_code_prefix, page_num), method='POST',
                             callback=self.parse_page, meta={'securityCodePrefix': security_code_prefix, 'pageNum': page_num, 'pageCount': page_count})

    def page_url(self, security_code_prefix, page_num):
        return 'http://www.cninfo.com.cn/new/disclosure?column={0}se_latest&pageNum={1}&pageSize=20'.format(security_code_prefix.lower(), page_num)

    def parse_page(self, response):
        security_code_prefix, page_num, page_count = response.meta['securityCodePrefix'], response.meta['pageNum'], response.meta['pageCount']
        all_announcements = json_loads(response.body.decode('utf-8'))['classifiedAnnouncements']
        for announcements in all_announcements:
            for announcement in announcements:
                security_code = '{0}{1}'.format(security_code_prefix, announcement['secCode'])
                file_url = 'http://www.cninfo.com.cn/{0}'.format(announcement['adjunctUrl'])
                if AnnouncementFile.exists(self.db, file_url):
                    return
                yield AnnouncementItem(security_code=security_code, company_name=announcement['secName'],
                                       title=announcement['announcementTitle'], announcement_time=announcement['announcementTime'],
                                       source='CNINFO', file_urls=[file_url], referer='')
        if page_num < page_count:
            page_num = page_num + 1
            yield scrapy.Request(url=self.page_url(security_code_prefix, page_num), method='POST',
                                 callback=self.parse_page, meta={'securityCodePrefix': security_code_prefix, 'pageNum': page_num, 'pageCount': page_count})
