from objects.globals import dp, bot

from aiogram.types import (
        Message,              CallbackQuery, 
        InlineKeyboardMarkup, InlineKeyboardButton
        )

from db_models.Resume import Resume

@dp.message_handler(lambda message: message.text == "Мои резюме")
async def create_resume(message: Message):
    all_resume = await Resume.objects.filter(user_id=message.from_user.id).all()
    
    if len(all_resume) == 0:
        return await message.answer(text="Резюме отсутствуют!")

    for resume in all_resume:
        globals()[str(resume.id)] = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Удалить", callback_data=f"delete-resume_{resume.id}")]
            ]
        ) 

        await message.answer(
            text=f"Уникальный Id: <code>{resume.id}</code>\n"
            f"Имя компании: {resume.company}\n"
            f"Должность: {resume.position}\n"
            f"Опыт работы: {resume.experience}\n"
            f"Результаты: {resume.results}\n"
            f"Причина увольнения: {resume.dismissal}", 
            reply_markup=globals()[str(resume.id)]
        )
        
@dp.callback_query_handler(lambda query: query.data.startswith(("delete-resume")))
async def delete_resume(query: CallbackQuery):

    get_resume = await Resume.objects.get(id=int(query.data.split("_")[1]))
    await get_resume.delete()

    return await bot.edit_message_text(
        chat_id=query.from_user.id, 
        message_id=query.message.message_id, 
        text="Резюме успешно удалено!"
    )