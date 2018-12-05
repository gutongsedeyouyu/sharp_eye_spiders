import config
from sharp_eye_spiders.pipelines import _engine, BaseModel, _database, AnnouncementDocument


BaseModel.metadata.create_all(_engine)
db = _database
