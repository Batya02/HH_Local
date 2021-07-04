from orm import Model, Integer, String, DateTime
from objects.globals import db, metadata

from datetime import datetime as dt

class Employer(Model):
    __tablename__ = "employers"
    __database__ = db
    __metadata__ = metadata

    id           = Integer(primary_key=True)
    user_id      = Integer()
    created      = DateTime(default=dt.now())
    name_company = String(max_length=255)
    fio          = String(max_length=255)
    profile      = String(max_length=255)
    adress       = String(max_length=255) 
    phone        = String(max_length=50)
    email        = String(max_length=255)
    url          = String(max_length=255)