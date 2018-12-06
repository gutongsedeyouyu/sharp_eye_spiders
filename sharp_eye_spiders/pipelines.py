# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime

import scrapy
from scrapy.pipelines.files import FilesPipeline
from sqlalchemy import create_engine, Column, BigInteger, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import config
from sharp_eye_spiders.items import AnnouncementItem


_engine = create_engine('mysql+pymysql://{3}:{4}@{0}:{1}/{2}?charset=utf8mb4'
                        .format(config.MYSQL_HOST, config.MYSQL_PORT, config.MYSQL_DATABASE,
                                config.MYSQL_USER, config.MYSQL_PASSWORD),
                        echo=config.MYSQL_ECHO)
_database = sessionmaker(bind=_engine)()
BaseModel = declarative_base()


class AnnouncementFile(BaseModel):
    __tablename__ = 'announcementfile'
    id = Column('id', BigInteger, primary_key=True)
    securityCode = Column('securitycode', String(16))
    companyName = Column('companyname', String(32))
    title = Column('title', String(128))
    announcementTime = Column('announcementTime', DateTime)
    fileUrl = Column('filelurl', String(256), unique=True)
    originalUrl = Column('originalurl', String(256), unique=True)
    createTime = Column('createtime', DateTime)


class AnnouncementPipeline(FilesPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = sessionmaker(bind=_engine)()

    def get_media_requests(self, item, info):
        for image_url in item['file_urls']:
            yield scrapy.Request(image_url, headers={'Referer': item['referer']})

    def item_completed(self, results, item, info):
        if not isinstance(item, AnnouncementItem):
            return item
        for ok, result in results:
            if not ok:
                continue
            if self.db.query(AnnouncementFile).filter(AnnouncementFile.originalUrl == result['url']).count() > 0:
                continue
            announcement = AnnouncementFile(securityCode=item['security_code'], companyName=item['company_name'],
                                            title=item['title'],
                                            announcementTime=datetime.fromtimestamp(int(item['announcement_time']) / 1000),
                                            fileUrl=result['url'], originalUrl=result['url'],
                                            createTime=datetime.now())
            self.db.add(announcement)
            self.db.commit()
        return super().item_completed(results, item, info)
