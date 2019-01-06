from sharp_eye_spiders.models import _engine, BaseModel, _database, Company, AnnouncementFile


BaseModel.metadata.create_all(_engine)
db = _database
