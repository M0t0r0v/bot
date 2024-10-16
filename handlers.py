from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import builder
from states import Registration

router = Router()


# Обработчик команды /start
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(
        "Привет! Вот мои кнопки:", reply_markup=builder.as_markup()
    )


# Обработчик для кнопки "Регистрация"
@router.message(F.text == "Регистрация")
async def reg_action(message: Message, state: FSMContext):
    await message.answer(
        "Введите вашу Фамилию, Имя и Отчество одним сообщением (через пробел):"
    )
    await state.set_state(Registration.waiting_for_full_name)


# Обработка ввода фамилии, имени и отчества
@router.message(Registration.waiting_for_full_name)
async def get_full_name(message: Message, state: FSMContext):
    full_name = message.text.split()

    if len(full_name) < 2:
        await message.answer(
            "Пожалуйста, введите как минимум Фамилию и Имя через пробел."
        )
        return

    surname = full_name[0]
    name = full_name[1]
    patronymic = full_name[2] if len(full_name) > 2 else ""

    await message.answer(
        f"Вы зарегистрированы как: {surname} {name} {patronymic}"
    )
    await state.clear()


# Обработчик для кнопки "Продолжить"
@router.message(F.text == "Продолжить")
async def login(message: Message):
    user_id = message.from_user.id
    await message.answer(
        f"Пользователь ID: {user_id} нажал кнопку Продолжить"
    )


# Обработчик команды /get_user_info
@router.message(Command("get_user_info"))
async def get_user_info(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    member = await message.bot.get_chat_member(chat_id, user_id)

    user_info = (
        f"Имя: {member.user.full_name}\n"
        f"Username: @{member.user.username}\n"
        f"ID пользователя: {member.user.id}\n"
        f"Статус в чате: {member.status}"
    )

    await message.answer(user_info)
