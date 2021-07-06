from flask import Flask, render_template 

from databases import Database
from sqlalchemy import MetaData, create_engine

from objects import globals

import asyncio

from json import loads

async def main():

    with open(r"config.json") as read_config:
        globals.config = loads(read_config.read())

    globals.app = Flask(__name__)
    globals.app.config['SECRET_KEY'] = globals.config["SECRET_KEY"]
    globals.app.config['TEMPLATES_AUTO_RELOAD'] = True 

    #Database
    globals.db = Database("sqlite:///../_db/HH.sqlite")
    globals.metadata = MetaData()

    globals.db_engine = create_engine(str(globals.db.url))
    globals.metadata.create_all(globals.db_engine)

    import actions

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    globals.app.run(host="0.0.0.0", debug=True)