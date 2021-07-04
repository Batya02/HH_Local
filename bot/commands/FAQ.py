from objects.globals import dp 

from aiogram.types import Message

@dp.message_handler(lambda message: message.text == "🔗FAQ")
async def FAQ(message: Message):
    with open(r"temp/FAQ.txt", "r", encoding="utf-8") as load_FAQ:
        FAQ = load_FAQ.read()

    return await message.answer(
        text=FAQ
    )