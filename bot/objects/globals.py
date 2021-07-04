from aiogram import Bot, Dispatcher

from databases import Database
from sqlalchemy import MetaData

bot:Bot = None
dp:Dispatcher = None
config:dict = {}

db:Database = None
metadata:MetaData = None
db_engine = None