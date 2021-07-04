from objects.globals import dp
from aiogram.types import Message

from aiogram.dispatcher.storage import FSMContext

#@dp.message_handler(commands="reset")
async def reset(message: Message, state:FSMContext):
    await state.finish()
    await message.answer(
        text=f"Операция отменена!"
        f"Начать регистрацию заново: /start"
    )