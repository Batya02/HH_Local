from objects.globals import dp
from aiogram.types import Message

from db_models.Employer import Employer
from db_models.Candidat import Candidat

@dp.message_handler(lambda message: message.text == "Мой профиль (Работодатель)")
async def my_profile(message: Message):

    profile_data = await Employer.objects.filter(user_id=message.from_user.id).all()
    if profile_data == []:
            return await message.answer(
                    text="Аккаунт был удалён!"
            )

    profile_data = profile_data[0]
    
    return await message.answer(
            text=f"Уникальный Id: <code>{profile_data.user_id}</code>\n"
            f"Имя компании: {profile_data.name_company}\n"
            f"ФИО: {profile_data.fio}\n"
            f"Профиль деятельности: {profile_data.profile}\n"
            f"Адрес: {profile_data.adress}\n"
            f"Телефон: {profile_data.phone}\n"
            f"Почта: {profile_data.email}\n"
            f"Ссылка: {profile_data.url}"
    )

@dp.message_handler(lambda message: message.text == "Мой профиль (Кандидат)")
async def my_profile_(message: Message):
    profile_data = await Candidat.objects.filter(user_id=message.from_user.id).all()
    if profile_data == []:
            return await message.answer(
                    text="Аккаунт был удалён!"
            )
            
    profile_data = profile_data[0]

    return await message.answer(
            text=f"Уникальный Id: <code>{profile_data.user_id}</code>\n"
            f"ФИО: {profile_data.fio}\n"
            f"Дата рождения: {profile_data.date_born}\n"
            f"Адрес: {profile_data.date_born}\n"
            f"Почта: {profile_data.email}\n"
            f"Телефон: {profile_data.phone}\n"
            f"Ссылка: {profile_data.url}"
    )