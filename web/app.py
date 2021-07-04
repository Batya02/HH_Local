from flask import Flask, render_template 

from databases import Database
from sqlalchemy import MetaData, create_engine

from objects import globals

globals.app = Flask("/var/www/")
globals.app.config['SECRET_KEY'] = "top_programmer"
globals.app.config['TEMPLATES_AUTO_RELOAD'] = True 

#Database
globals.db = Database("sqlite:///root/HH_Local/_db/HH.sqlite")
globals.metadata = MetaData()

globals.db_engine = create_engine(str(globals.db.url))
globals.metadata.create_all(globals.db_engine)

import asyncio

async def main():
    import actions

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    globals.app.run(host="127.0.0.1", port="5000")