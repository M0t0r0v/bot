from aiogram.utils.keyboard import ReplyKeyboardBuilder

builder = ReplyKeyboardBuilder()
builder.button(text="Регистрация")
builder.button(text="Продолжить")
builder.adjust(2)
