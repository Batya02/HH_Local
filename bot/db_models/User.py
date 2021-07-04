from orm import Model, Integer, String, DateTime, Boolean
from objects.globals import db, metadata

from datetime import datetime as dt

class User(Model):
    __tablename__ = "users"
    __database__ = db
    __metadata__ = metadata

    id           = Integer(primary_key=True)
    user_id      = Integer()
    username     = String(max_length=255, default=None)
    created      = DateTime(default=dt.now())
    type         = String(max_length=8, default=None)
    verification = Boolean(default=0)
    spam         = Boolean(default=0)