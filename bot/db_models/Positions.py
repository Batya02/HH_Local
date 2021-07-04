from orm import Model, Integer, String
from objects.globals import db, metadata

class Positions(Model):
    __tablename__ = "positions"
    __database__ = db
    __metadata__ = metadata

    id   = Integer(primary_key=True)
    name = String(max_length=255)