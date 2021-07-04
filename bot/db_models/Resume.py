from orm import Model, Integer, String, DateTime
from objects.globals import db, metadata

from datetime import datetime as dt

class Resume(Model):
    __tablename__ = "resume"
    __database__ = db
    __metadata__ = metadata

    id         = Integer(primary_key=True)
    user_id    = Integer()
    company    = String(max_length=255)
    position   = String(max_length=255)
    experience = String(max_length=255)
    results    = String(max_length=255)
    dismissal  = String(max_length=255)
    created    = DateTime(default=dt.now())