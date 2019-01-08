import scrapy
from datetime import datetime
from json import loads as json_loads

from sharp_eye_spiders.items import AnnouncementItem
from sharp_eye_spiders.models import _database, Company, AnnouncementFile


class CninfoSpider(scrapy.Spider):
    name = "chinamoney"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = _database
        self.companies = Company.list_all(self.db)

    def start_requests(self):
        yield scrapy.FormRequest(url='http://www.chinamoney.com.cn/ags/ms/cm-u-notice-md/ReportAndNotice',
                                 formdata={'entyDefinedCode': '900453', 'publishCode': '1', 'secondType': '1002', 'pageNo': '1', 'pageSize': '15'},
                                 callback=self.parse_report_and_notice, method='POST')

    def parse_report_and_notice(self, response):
        result = json_loads(response.body.decode())
        for report in result['data']['resultList']:
            yield AnnouncementItem(company_id=None, security_code='', company_name='武汉正通联合',
                                   title=report['title'], announcement_time=datetime.strptime(report['releaseDate'][:-2], '%Y-%m-%d %H:%M:%S').timestamp(),
                                   source='CHINAMONEY',
                                   file_urls=['{0}/dqs/cm-s-notice-query/fileDownLoad.do?mode=open&contentId={1}&priority=0'.format('http://www.chinamoney.com.cn', report['contentId'])],
                                   referer='')
