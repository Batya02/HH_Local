from objects.globals import dp, bot 

from aiogram.types import (
        Message,              CallbackQuery, 
        InlineKeyboardMarkup, InlineKeyboardButton
        )   

from aiogram.dispatcher.storage import FSMContext

from states.states import Resume_Steps

from db_models.Positions import Positions
from db_models.Resume import Resume

EXPERIENCE = [
                [InlineKeyboardButton(text="Менее года",  callback_data="-exp_Менее года")], 
                [InlineKeyboardButton(text="Год",         callback_data="-exp_Год")], 
                [InlineKeyboardButton(text="Два",         callback_data="-exp_Два")], 
                [InlineKeyboardButton(text="Более 3 лет", callback_data="-exp_Более 3 лет")], 
                [InlineKeyboardButton(text="Более 5 лет", callback_data="-exp_Более 5 лет")]
                ]

@dp.message_handler(lambda message: message.text == "Создать резюме")
async def create_resume(message: Message):

    resume_check_count = await Resume.objects.filter(user_id=message.from_user.id).all()
    
    if len(resume_check_count) == 3:
        return await message.answer(text="Максимальное количество резюме - 3")
    
    await message.answer(
        text="Пожалуйста укажите название компании, в которой вы работали:"
    )

    await Resume_Steps.get_company_targ.set()

@dp.message_handler(state=Resume_Steps.get_company_targ)
async def get_company_targ(message: Message, state:FSMContext):
    await state.finish()

    await state.update_data(get_company_var=message.text)

    positions = await Positions.objects.all()

    positions_buttons = InlineKeyboardMarkup()

    for position in positions:
        positions_buttons.add(InlineKeyboardButton(text=position.name, callback_data=f"-pos_{position.name}"))
    
    positions_buttons.add(InlineKeyboardButton(text="Указать должность", callback_data="point_out_-pos"))

    return await message.answer(
        text="Пожалуйста выберите должность, которую вы занимали или выберите действие", 
        reply_markup=positions_buttons
    )


@dp.callback_query_handler(lambda query: query.data.startswith(("-pos")))
async def get_buttons_position(query: CallbackQuery, state:FSMContext):
    position = query.data.split("_")[1]
    await state.update_data(get_position_var=position)

    experience_buttons = InlineKeyboardMarkup(
        inline_keyboard=EXPERIENCE
    )
    
    await bot.edit_message_text(
        chat_id = query.from_user.id, 
        message_id = query.message.message_id,
        text="Выберите опыт работы", 
        reply_markup=experience_buttons
    )

@dp.callback_query_handler(lambda query: query.data == "point_out_-pos")
async def point_out_position_(query: CallbackQuery):
    await bot.edit_message_text(
        chat_id = query.from_user.id, 
        message_id = query.message.message_id,
        text="Пожалуйста укажите должность, которую вы занимали:"
    )

    await Resume_Steps.get_position_targ.set()

@dp.message_handler(state=Resume_Steps.get_position_targ)
async def get_position_targ(message: Message, state:FSMContext):
    data = await state.get_data()
    await state.finish()
    await state.update_data(get_company_var=data["get_company_var"]) #Override company var
    await state.update_data(get_position_var=message.text)

    experience_buttons = InlineKeyboardMarkup(
        inline_keyboard=EXPERIENCE
    )
    
    return await message.answer(
        text="Выберите опыт работы", 
        reply_markup=experience_buttons
    )

@dp.callback_query_handler(lambda query: query.data.startswith(("-exp")))
async def get_results_targ(query: CallbackQuery, state: FSMContext):
    await state.update_data(get_experience_var=query.data.split("_")[1])

    await bot.edit_message_text(
        chat_id=query.from_user.id, 
        message_id=query.message.message_id, 
        text="Укажите в одном сообщении, каких результатов Вам удалось добиться на этой должности:"
    )

    await Resume_Steps.get_results_targ.set()

@dp.message_handler(state=Resume_Steps.get_results_targ)
async def get_results_targ(message: Message, state: FSMContext):
    await state.update_data(get_results_var=message.text)

    await message.answer(text="Укажите в одном сообщении, почему вы решили уволиться с этого места работы:") 

    await Resume_Steps.get_dismissal_targ.set()

@dp.message_handler(state=Resume_Steps.get_dismissal_targ)
async def get_dismissal_targ(message: Message, state:FSMContext):
    await state.update_data(get_dismissal_var=message.text)

    data = await state.get_data()
    
    await Resume.objects.create(
        user_id    = message.from_user.id, 
        company    = data["get_company_var"], 
        position   = data["get_position_var"], 
        experience = data["get_experience_var"], 
        results    = data["get_results_var"], 
        dismissal  = data["get_dismissal_var"]
    )

    await state.finish()
    await message.answer(text="Резюме успешно создано!")