from states.states import Application_Steps
from objects.globals import dp, bot

from aiogram.dispatcher.storage import FSMContext

from aiogram.types import (
        Message,              CallbackQuery, 
        InlineKeyboardMarkup, InlineKeyboardButton
        )

from db_models.Positions import Positions
from db_models.Application import Application

EXPERIENCE = [
        [InlineKeyboardButton(text="Неважно",   callback_data="exp-year_Неважно")], 
        [InlineKeyboardButton(text="От 1 года", callback_data="exp-year_От 1 года")], 
        [InlineKeyboardButton(text="От 2 лет",  callback_data="exp-year_От 2 лет")], 
        [InlineKeyboardButton(text="От 5 лет",  callback_data="exp-year_От 5 лет")], 
        [InlineKeyboardButton(text="От 10 лет", callback_data="exp-year_От 10 лет")]
        ]

AGES = [
        [InlineKeyboardButton(text="Неважно", callback_data="age_Неважно")], 
        [InlineKeyboardButton(text="18-25",   callback_data="age_18-25")], 
        [InlineKeyboardButton(text="25-35",   callback_data="age_25-35")], 
        [InlineKeyboardButton(text="35-40",   callback_data="age_35-40")], 
        [InlineKeyboardButton(text="40+",     callback_data="age_40+")], 
        [InlineKeyboardButton(text="Далее",   callback_data="continue_age")]
        ]

WAGE = [
        [InlineKeyboardButton(text="До 15 000",       callback_data="wage_До 15 000")], 
        [InlineKeyboardButton(text="15 000 - 20 000", callback_data="wage_15 000 - 20 000")], 
        [InlineKeyboardButton(text="20 000 - 25 000", callback_data="wage_20 000 - 25 000")], 
        [InlineKeyboardButton(text="25 000 - 30 000", callback_data="wage_25 000 - 30 000")], 
        [InlineKeyboardButton(text="30 000 - 35 000", callback_data="wage_30 000 - 35 000")], 
        [InlineKeyboardButton(text="Указать ЗП",      callback_data="point_out_wage")]
        ]

@dp.message_handler(lambda message: message.text == "Создать заявку")
async def create_application(message: Message):

    positions = await Positions.objects.all()
    
    position_buttons = InlineKeyboardMarkup()

    if positions == []:pass
    else:
        for position in positions:
            position_buttons.add(InlineKeyboardButton(text=position.name, callback_data=f"position_{position.name}"))

    position_buttons.add(InlineKeyboardButton(text="Указать должность", callback_data=f"point_out_position"))

    await message.answer(
        text="Выберите должность или действие", 
        reply_markup=position_buttons
    )

@dp.callback_query_handler(lambda query: query.data.startswith(("position")))
async def take_position(query: CallbackQuery, state:FSMContext):

    position = query.data.split("_")[1]
    await state.update_data(get_position_var=position)
    experience_total = InlineKeyboardMarkup(
        inline_keyboard=EXPERIENCE
    )

    return await bot.send_message(
        query.from_user.id, 
        text="Выберите опыт работы соискателя", 
        reply_markup=experience_total
    )

@dp.callback_query_handler(lambda query: query.data == "point_out_position")
async def point_out_position(query: CallbackQuery):
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id, 
        text="Введите должность:"
    )

    await Application_Steps.get_position_targ.set()

@dp.message_handler(state=Application_Steps.get_position_targ)
async def get_position_targ(message: Message, state:FSMContext):
    await state.finish()
    await state.update_data(get_position_var=message.text)
    experience_total = InlineKeyboardMarkup(
        inline_keyboard=EXPERIENCE
    )

    return await message.answer(
        text="Выберите опыт работы соискателя", 
        reply_markup=experience_total
    )

@dp.callback_query_handler(lambda query: query.data.startswith(("exp-year")))
async def get_experience_targ(query: CallbackQuery, state:FSMContext):
    experience = query.data.split("_")[1]
    
    await state.update_data(get_experience_var=experience)

    age_buttons = InlineKeyboardMarkup(
        inline_keyboard=AGES
    )

    return await bot.send_message(
        query.from_user.id, 
        text="Выберите возраст соискателя", 
        reply_markup=age_buttons
    )

@dp.callback_query_handler(lambda query: query.data.startswith(("age")))
async def get_age_targ(query: CallbackQuery, state: FSMContext):
    age = query.data.split("_")[1]
    
    if age == "Неважно":
        await state.update_data(get_age_var=age)
        await bot.send_message(
                query.from_user.id, 
                text="Укажите типовые задачи, которые должен будет выполнять Ваш сотрудник:"
        )

        await Application_Steps.get_tasks_targ.set()

    else:
        if not age in AGES:AGES.append(age); await query.answer(text=f"Вы выбрали {AGES}")
        else:await query.answer(text="Находится в списке выбора!")


@dp.callback_query_handler(lambda query: query.data == "continue_age")
async def continue_age(query: CallbackQuery, state: FSMContext):
    if AGES == []:
        return await query.answer(text="Вы не выбрали ни одного возраста!")
    
    else:
        ages_string = "; ".join(AGES)
        await state.update_data(get_age_var=ages_string)
        AGES.clear()
    
    wage_buttons = InlineKeyboardMarkup(
        inline_keyboard=WAGE
    )

    return await bot.send_message(
        query.from_user.id, 
        text="Заработная плата соискателя", 
        reply_markup=wage_buttons
    )

@dp.callback_query_handler(lambda query: query.data.startswith(("wage")))
async def get_wage_targ(query: CallbackQuery, state:FSMContext):
    wage = query.data.split("_")[1]

    await state.update_data(get_wage_var=wage)

    await bot.send_message(
        query.from_user.id, 
        text="Укажите типовые задачи, которые должен будет выполнять Ваш сотрудник:"
    )

    await Application_Steps.get_tasks_targ.set()

@dp.message_handler(state=Application_Steps.get_tasks_targ)
async def get_tasks_targ(message: Message, state:FSMContext):
    await state.update_data(get_tasks_var=message.text)

    data = await state.get_data()

    check_application = await Application.objects.filter(
            user_id    = message.from_user.id, 
            position   = data["get_position_var"], 
            experience = data["get_experience_var"], 
            age        = data["get_age_var"], 
            wage       = data["get_wage_var"], 
            tasks      = data["get_tasks_var"]
            ).all()

    if check_application != []:
        return await message.answer(text="Такая заявка уже существует!")

    await Application.objects.create(
            user_id    = message.from_user.id, 
            position   = data["get_position_var"], 
            experience = data["get_experience_var"],
            age        = data["get_age_var"], 
            wage       = data["get_wage_var"], 
            tasks      = data["get_tasks_var"]
    )
    await state.finish()
    return await message.answer(text="Заявка успешно создана!")