from orm import Model, Integer, String, DateTime
from objects.globals import db, metadata

from datetime import datetime as dt

class Application(Model):
    __tablename__ = "applications"
    __database__ = db
    __metadata__ = metadata

    id         = Integer(primary_key=True)
    user_id    = Integer()
    position   = String(max_length=255)
    experience = String(max_length=255)
    age        = String(max_length=60)
    wage       = String(max_length=255)
    tasks      = String(max_length=255)
    created    = DateTime(default=dt.now())