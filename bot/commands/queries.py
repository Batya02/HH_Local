from objects.globals import dp, bot 

from aiogram.dispatcher.storage import FSMContext

from aiogram.types import (
        Message,       InlineKeyboardMarkup,
        CallbackQuery, InlineKeyboardButton 
        )

from db_models.Employer import Employer
from db_models.Candidat import Candidat
from db_models.User     import User

from states.states import Employer_Steps, Candidat_Steps

from commands.reset import reset

#EMPLOYER registration steps
@dp.callback_query_handler(lambda query: query.data == "i'm_employer")
async def i_am_employer(query: CallbackQuery):
    check = await Employer.objects.filter(user_id=query.from_user.id).all()
    
    if check != []:
        return await bot.send_message(
            query.from_user.id, 
            text="Аккаунт уже существует!"
        )

    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id, 
        text=f"Для завершения регистрации на любом этапе, используйте команду /reset\n"
        f"Укажите название компании:"
    )
    await Employer_Steps.get_name_company_targ.set()

@dp.message_handler(state=Employer_Steps.get_name_company_targ)
async def get_name_company(message: Message, state: FSMContext):
    if message.text == "/reset":
        return await reset(message, state)

    await state.update_data(get_name_company_var=message.text)
    await message.answer(
        text="Введите профиль деятельности:"
    )
    await Employer_Steps.get_profile_targ.set()

@dp.message_handler(state=Employer_Steps.get_profile_targ)
async def get_profile_targ(message: Message, state: FSMContext):
    if message.text == "/reset":
        return await reset(message, state)

    await state.update_data(get_profile_var=message.text)
    await message.answer(
        text="Введите адрес:"
    )
    await Employer_Steps.get_adress_targ.set()

@dp.message_handler(state=Employer_Steps.get_adress_targ)
async def get_adress_targ(message: Message, state: FSMContext):
    if message.text == "/reset":
        return await reset(message, state)

    await state.update_data(get_adress_var=message.text)
    await message.answer(
        text="Введите ФИО контактного лица:"
    )
    await Employer_Steps.get_fio_targ.set()

@dp.message_handler(state=Employer_Steps.get_fio_targ)
async def get_fio_targ(message: Message, state:FSMContext):
    if message.text == "/reset":
        return await reset(message, state)

    await state.update_data(get_fio_var=message.text)
    await message.answer(
        text="Введите контактный номер телефона(без лишних знаков):"
    )
    await Employer_Steps.get_phone_targ.set()

@dp.message_handler(state=Employer_Steps.get_phone_targ)  
async def get_phone_targ(message: Message, state: FSMContext):
    if message.text == "/reset":
        return await reset(message, state)

    await state.update_data(get_phone_var=message.text)
    await message.answer(
        text="Введите почту:"
    )
    await Employer_Steps.get_email_targ.set()

@dp.message_handler(state=Employer_Steps.get_email_targ)
async def get_email_targ(message: Message, state: FSMContext):
    if message.text == "/reset":
        return await reset(message, state)

    await state.update_data(get_email_var=message.text)
    await message.answer(
        text="Ссылка на сайт компании или профиль в соцсетях:"
    )

    await Employer_Steps.get_url_targ.set()

@dp.message_handler(state=Employer_Steps.get_url_targ)
async def get_url_targ(message: Message, state: FSMContext):
    if message.text == "/reset":
        return await reset(message, state)
        
    await state.update_data(get_url_var=message.text) 

    data = await state.get_data() # Get all states variables

    await Employer.objects.create(
        user_id      = message.from_user.id, 
        name_company = data["get_name_company_var"],
        fio          = data["get_fio_var"], 
        profile      = data["get_profile_var"], 
        adress       = data["get_adress_var"], 
        phone        = data["get_phone_var"], 
        email        = data["get_email_var"], 
        url          = data["get_url_var"]
    )

    update_type = await User.objects.get(user_id=message.from_user.id)
    await update_type.update(type="employer")

    await message.answer(
        text=f"Регистрация завершена!\n"
        f"Для продолжения нажмите на /start"
    )
    await state.finish()

#CANDIDAT registration steps
@dp.callback_query_handler(lambda query: query.data == "i'm_candidat")
async def i_am_candidat(query: CallbackQuery):
    check = await Candidat.objects.filter(user_id=query.from_user.id).all()

    if check != []:
        return await bot.send_message(
            query.from_user.id, 
            text="Аккаунт уже существует!"
        )

    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id, 
        text=f"Для завершения регистрации на любом этапе, используйте команду /reset\n"
        f"Введите фамилию и имя:"
    )
    await Candidat_Steps.get_fio_targ.set()

@dp.message_handler(state=Candidat_Steps.get_fio_targ)
async def get_fio_targ_(message: Message, state: FSMContext):
    if message.text == "/reset":
        return await reset(message, state)

    await state.update_data(get_fio_var=message.text)
    await message.answer(
        text="Введите дату рождения:"
    )
    await Candidat_Steps.get_date_born_targ.set()

@dp.message_handler(state=Candidat_Steps.get_date_born_targ)
async def get_date_born_targ_(message: Message, state: FSMContext):
    if message.text == "/reset":
        return await reset(message, state)

    await state.update_data(get_date_born_var=message.text)
    await message.answer(
        text="Введите адрес:"
    )
    await Candidat_Steps.get_adress_targ.set()

@dp.message_handler(state=Candidat_Steps.get_adress_targ)
async def get_adress_targ(message: Message, state: FSMContext):
    if message.text == "/reset":
        return await reset(message, state)

    await state.update_data(get_adress_var=message.text)
    await message.answer(
        text="Введите email:"
    )
    await Candidat_Steps.get_email_targ.set()

@dp.message_handler(state=Candidat_Steps.get_email_targ)
async def get_email_targ_(message: Message, state: FSMContext):
    if message.text == "/reset":
        return await reset(message, state)

    await state.update_data(get_email_var=message.text)
    await message.answer(
        text="Введите телефон:"
    )
    await Candidat_Steps.get_phone_targ.set()

@dp.message_handler(state=Candidat_Steps.get_phone_targ)
async def get_phone_targ_(message: Message, state: FSMContext):
    if message.text == "/reset":
        return await reset(message, state)

    await state.update_data(get_phone_var=message.text)
    await message.answer(
        text="Ссылка на профиль в соцсетях:"
    )
    await Candidat_Steps.get_url_targ.set()

@dp.message_handler(state=Candidat_Steps.get_url_targ)
async def get_url_targ_(message: Message, state: FSMContext):
    if message.text == "/reset":
        return await reset(message, state)

    await state.update_data(get_url_var=message.text) # Get all states variables

    data = await state.get_data()

    await Candidat.objects.create(
        user_id   = message.from_user.id, 
        fio       = data["get_fio_var"], 
        date_born = data["get_date_born_var"], 
        adress    = data["get_adress_var"], 
        email     = data["get_email_var"], 
        phone     = data["get_phone_var"],
        url       = data["get_url_var"]
    )

    update_type = await User.objects.get(user_id=message.from_user.id)
    await update_type.update(type="candidat")

    await message.answer(
        text=f"Регистрация завершена!\n"
        f"Для продолжения нажмите на /start"
    )
    await state.finish()