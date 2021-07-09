from databases import Database
from sqlalchemy import MetaData

db:Database = None
metadata:MetaData = None
db_engine = None

app = None

config:dict = {}

ip_adress:str = ""

state_password = ""