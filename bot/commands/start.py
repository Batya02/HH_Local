from objects.globals import dp

from aiogram.types import (
        Message,              InlineKeyboardMarkup, 
        InlineKeyboardButton, ReplyKeyboardMarkup, 
        KeyboardButton)

from db_models.User import User

@dp.message_handler(commands = "start")
async def start(message: Message):

    data_user = await User.objects.filter(user_id=message.from_user.id).all()

    if data_user == []:
        if message.from_user.username == None:
            await User.objects.create(
                user_id=message.from_user.id
            )
        else:
            await User.objects.create(
                user_id=message.from_user.id, 
                username=message.from_user.username
            )
            
    check_type = await User.objects.get(user_id=message.from_user.id)
    
    work_types = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Работадатель", callback_data="i'm_employer")], 
            [InlineKeyboardButton(text="Соискатель", callback_data="i'm_candidat")]
        ]
    )

    if check_type.type == None or check_type.type == "Unknow":
        return await message.answer(
            text="🤖Привет! Я бот созданный для ...", 
            reply_markup=work_types
        ) 
    
    elif check_type.type == "employer":
        employer_actions = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Мой профиль (Работодатель)")], 
                [KeyboardButton(text="Создать заявку"), 
                 KeyboardButton(text="Мои заявки")],
                [KeyboardButton(text="Добавить ссылку на Google Documents")],
                [KeyboardButton(text="🔗FAQ")]
            ], 
            resize_keyboard=True
        )

        await message.answer(
            text="Выберите пункт", 
            reply_markup=employer_actions
        )

    elif check_type.type == "candidat":
        candidat_actions = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Мой профиль (Кандидат)")],
                [KeyboardButton(text="Создать резюме"), 
                 KeyboardButton(text="Мои резюме")],
                [KeyboardButton(text="Добавить ссылку на Google Documents")], 
                [KeyboardButton(text="🔗FAQ")]
            ], 
            resize_keyboard=True
        )

        await message.answer(
            text="Выберите пункт", 
            reply_markup=candidat_actions
        )