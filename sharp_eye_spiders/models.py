from datetime import datetime

from sqlalchemy import create_engine, Column, BigInteger, String, DateTime, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import config


_engine = create_engine('mysql+pymysql://{3}:{4}@{0}:{1}/{2}?charset=utf8mb4'.format(
                                config.MYSQL_HOST, config.MYSQL_PORT, config.MYSQL_DATABASE,
                                config.MYSQL_USER, config.MYSQL_PASSWORD),
                        echo=config.MYSQL_ECHO)
_database = sessionmaker(bind=_engine)()
BaseModel = declarative_base()


class Company(BaseModel):
    __tablename__ = 'company'
    id = Column('keyNo', String(32), primary_key=True)
    name = Column('name', String(100))
    securityCode = Column('stockNumber', String(100))
    isPublic = Column('isPublic', String(50))
    isChekctPublic = Column('isChekctPublic', String(50))
    isOnStock = Column('isOnStock', String(50))
    isChekctStock = Column('isChekctStock', String(50))

    @staticmethod
    def list_all(db):
        return [c for c in db.query(Company)]
    
    @staticmethod
    def list_public_not_checked(db):
        return [c for c in db.query(Company).filter(Company.isChekctPublic == None)]
    
    @staticmethod
    def list_stock_not_checked(db):
        return [c for c in db.query(Company).filter(Company.isChekctStock == None)]
    
    @staticmethod
    def list_stock(db):
        return [c for c in db.query(Company).filter(Company.isOnStock == '1')]


class AnnouncementFile(BaseModel):
    __tablename__ = 'announcement_file'
    id = Column('id', BigInteger, primary_key=True)
    companyId = Column('company_id', String(32))
    securityCode = Column('security_code', String(16))
    companyName = Column('company_name', String(32))
    title = Column('title', String(128))
    announcementTime = Column('announcement_time', DateTime)
    source = Column('source', String(16))
    isPublic = Column('is_public', Integer)
    isStock = Column('is_stock', Integer)
    negative = Column('negative', String(1))
    fileUrl = Column('file_url', String(256), unique=True)
    originalUrl = Column('original_url', String(256), unique=True)
    createTime = Column('create_time', DateTime)

    @staticmethod
    def exists(db, original_url):
        cursor = db.query(AnnouncementFile).filter(AnnouncementFile.originalUrl == original_url)
        return cursor.count() > 0

    @staticmethod
    def add(db, company_id, security_code, company_name, title, announcement_time, source, file_url, original_url):
        is_public = 1 if source in ('CHINAMONEY', ) else 0
        is_stock = 1 if source in ('CNINFO', ) else 0
        now = datetime.now()
        announcement = AnnouncementFile(companyId=company_id, securityCode=security_code, companyName=company_name,
                                        title=title, announcementTime=announcement_time,
                                        source=source, isPublic=is_public, isStock=is_stock, negative='',
                                        fileUrl=file_url, originalUrl=original_url,
                                        createTime=now)
        db.add(announcement)
        db.commit()
