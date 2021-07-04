from objects.globals import dp, bot

from aiogram.types import (
        Message,              CallbackQuery, 
        InlineKeyboardMarkup, InlineKeyboardButton
        )

from db_models.Application import Application

@dp.message_handler(lambda message: message.text == "Мои заявки")
async def my_applications(message: Message):

    my_applications = await Application.objects.filter(user_id=message.from_user.id).all()

    if my_applications == []:
        return await message.answer(text="Список заявок пуст!")

    for application in my_applications:
        globals()[str(application.id)] = InlineKeyboardMarkup(
            inline_keyboard = [
                [InlineKeyboardButton(text="Удалить", callback_data=f"app-off_{application.id}")]
            ]
        )

        await bot.send_message(
            message.from_user.id, 
            text=f"ID: {application.id}\n"
            f"Должность: {application.position}\n"
            f"Опыт работы: {application.experience}\n"
            f"Возраст соискателя: {application.age}\n"
            f"Заработная плата: {application.wage}\n"
            f"Требуемые задачи: {application.tasks}", 
            reply_markup=globals()[str(application.id)]
        ) 

@dp.callback_query_handler(lambda query: query.data.startswith(("app-off")))
async def app_off(query: CallbackQuery):
    app = await Application.objects.get(id=int(query.data.split("_")[1]))
    await app.delete()

    return await bot.edit_message_text(
        chat_id = query.from_user.id, 
        message_id = query.message.message_id, 
        text="Заявка успешно отменена!"
    )