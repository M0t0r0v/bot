import os
from dotenv import load_dotenv
from aiogram.utils.keyboard import ReplyKeyboardBuilder

load_dotenv()

def get_keyboard(user_id: int, registered: bool):
    builder = ReplyKeyboardBuilder()
    if not registered:
        builder.button(text="Регистрация")
    else:   
        builder.button(text="Продолжить")
    
    admin_ids = tuple(map(int, os.getenv('ADMIN_ID').split(',')))
    if user_id in admin_ids and registered:
        builder.button(text="Админ. панель")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)