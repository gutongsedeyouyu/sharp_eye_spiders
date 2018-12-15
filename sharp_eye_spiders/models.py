from datetime import datetime

from sqlalchemy import create_engine, Column, BigInteger, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import config


_engine = create_engine('mysql+pymysql://{3}:{4}@{0}:{1}/{2}?charset=utf8mb4'.format(
                                config.MYSQL_HOST, config.MYSQL_PORT, config.MYSQL_DATABASE,
                                config.MYSQL_USER, config.MYSQL_PASSWORD),
                        echo=config.MYSQL_ECHO)
_database = sessionmaker(bind=_engine)()
BaseModel = declarative_base()


class AnnouncementFile(BaseModel):
    __tablename__ = 'announcement_file'
    id = Column('id', BigInteger, primary_key=True)
    securityCode = Column('security_code', String(16))
    companyName = Column('company_name', String(32))
    title = Column('title', String(128))
    announcementTime = Column('announcement_time', DateTime)
    source = Column('source', String(16))
    fileUrl = Column('file_url', String(256), unique=True)
    originalUrl = Column('original_url', String(256), unique=True)
    createTime = Column('create_time', DateTime)

    @staticmethod
    def exists(db, original_url):
        cursor = db.query(AnnouncementFile).filter(AnnouncementFile.originalUrl == original_url)
        return cursor.count() > 0

    @staticmethod
    def add(db, security_code, company_name, title, announcement_time, file_url, original_url, source):
        now = datetime.now()
        announcement = AnnouncementFile(securityCode=security_code, companyName=company_name,
                                        title=title, announcementTime=announcement_time,
                                        source=source, fileUrl=file_url, originalUrl=original_url,
                                        createTime=now)
        db.add(announcement)
        db.commit()
