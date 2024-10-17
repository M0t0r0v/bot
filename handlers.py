from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot import TELEGRAM_TOKEN
from encrypt_decrypt import xor_encrypt_decrypt
from keyboards import builder
from models import SessionLocal, add_user
from states import Registration

router = Router()


async def get_db():
    async with SessionLocal() as session:
        yield session  # Создаём сессию


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

    chat_id = message.chat.id
    user_id = message.from_user.id
    member = await message.bot.get_chat_member(chat_id, user_id)
    full_name = ' '.join(full_name)

    async for db in get_db():
        await add_user(
            db,
            xor_encrypt_decrypt(member.user.username, TELEGRAM_TOKEN),
            xor_encrypt_decrypt(full_name, TELEGRAM_TOKEN),
        )

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
