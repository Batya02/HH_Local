from orm import Model, Integer, String, DateTime
from objects.globals import db, metadata

from datetime import datetime as dt

class Candidat(Model):
    __tablename__ = "candidats"
    __database__ = db
    __metadata__ = metadata

    id        = Integer(primary_key=True)
    user_id   = Integer()
    created   = DateTime(default=dt.now())
    fio       = String(max_length=255)
    date_born = String(max_length=255)
    adress    = String(max_length=255)
    email     = String(max_length=255)
    phone     = String(max_length=50)
    url       = String(max_length=255)