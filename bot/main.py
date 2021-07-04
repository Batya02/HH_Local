import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from objects import globals

from databases import Database
from sqlalchemy import MetaData, create_engine

from json import dumps, loads

from os.path import isfile

from loguru import logger

async def main():

    if not isfile(r"config.json"):
        with open(r"config.json", "w") as add_cfg:
            add_cfg.write(dumps(
                {
                    "token":"", 
                    "db_host":"", 
                    "db_name":"",
                    "db_user":"", 
                    "db_password":"", 
                    "db_port":5432
                }, indent=4
            ))
            add_cfg.close()
    
    with open(r"config.json", "r", encoding="utf-8") as load_cfg:
        globals.config = loads(load_cfg.read())
    
    logger.info("Configuration loaded!")

    #Telegram API
    globals.bot = Bot(token=globals.config["token"], parse_mode="html")
    globals.dp = Dispatcher(globals.bot, storage=MemoryStorage())

    #Database
    globals.db = Database("sqlite:///../_db/HH.sqlite")
    globals.metadata = MetaData()

    globals.db_engine = create_engine(str(globals.db.url))
    globals.metadata.create_all(globals.db_engine)

    bot_info = await globals.bot.get_me()
    logger.info(f"Start bot @{bot_info.username}")

    import commands

    await globals.dp.start_polling()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:pass