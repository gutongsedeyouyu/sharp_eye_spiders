from sharp_eye_spiders.models import _engine, BaseModel, _database, AnnouncementFile


BaseModel.metadata.create_all(_engine)
db = _database
