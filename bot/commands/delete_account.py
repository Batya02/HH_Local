from objects.globals import dp

from aiogram.types import (
    Message, ReplyKeyboardMarkup, 
    KeyboardButton
    )

from db_models.Employer import Employer 
from db_models.Candidat import Candidat
from db_models.User import User

@dp.message_handler(commands="delete")
async def delete_account(message: Message):

    check_for_employer = await Employer.objects.filter(user_id=message.from_user.id).all()
    check_for_candidat = await Candidat.objects.filter(user_id=message.from_user.id).all()

    if check_for_employer == [] and check_for_candidat == []:
        return await message.answer(
            text=f"Для начала нужно создать аккаунт!\n"
            f"Нажмите /start для создания."
        )
    
    else:
        if check_for_employer != []:
            del_employer = await Employer.objects.get(user_id=message.from_user.id)
            await del_employer.delete()
        
        elif check_for_candidat != []:
            del_candidat= await Candidat.objects.get(user_id=message.from_user.id)
            await del_candidat.delete()
        
        update_type = await User.objects.get(user_id=message.from_user.id)
        await update_type.update(type="Unknow")

        FAQ = ReplyKeyboardMarkup(
            keyboard=[ 
                [KeyboardButton(text="🔗FAQ")]
            ], 
            resize_keyboard=True
        )

        return await message.answer(
            text=f"Аккаунт успешно удалён!\n"
            "Для создания нового нажмите /start", 
            reply_markup=FAQ
        )