from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

from bot import TELEGRAM_TOKEN
from encrypt_decrypt import xor_encrypt_decrypt
from keyboards import get_keyboard
from models import SessionLocal, add_user, get_all_users, get_user_registered
from states import Registration
from validation import validate_full_name
from chat_link import create_invite_link


# from sqlalchemy.ext.asyncio import AsyncSession


router = Router()


async def get_db():
    async with SessionLocal() as session:
        yield session  # Создаём сессию


# Обработчик команды /start
@router.message(Command("start"))
async def send_welcome(message: Message):
    telegram_id = message.from_user.id
    async for db in get_db():
        registered = await get_user_registered(db, telegram_id)
    keyboard = get_keyboard(telegram_id, registered)
    await message.answer("Добро пожаловать!", reply_markup=keyboard)


# Обработчик для кнопки "Регистрация"
@router.message(F.text == "Регистрация")
async def reg_action(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    async for db in get_db():
        registered = await get_user_registered(db, telegram_id)
        if registered:
            await message.answer("Вы уже зарегистрированы.")
            return
        await message.answer(
            "Введите вашу Фамилию, Имя и Отчество одним сообщением (через пробел):"
        )
        await state.set_state(Registration.waiting_for_full_name)


@router.message(Registration.waiting_for_full_name)
async def process_full_name(message: Message, state: FSMContext):
    # Сохранить ФИО пользователя
    await state.update_data(full_name=message.text)

    # Запросить SberID и ожидание ввода пользователя SberID
    await message.answer("Введите ваш SberID:")
    await state.set_state(Registration.waiting_for_sber_id)


@router.message(Registration.waiting_for_sber_id)
async def process_sber_id(message: Message, state: FSMContext):
    # Сохранить SberID
    await state.update_data(sber_id=message.text)

    # Запросить номер команды
    await message.answer("Введите номер вашей команды:")
    await state.set_state(Registration.waiting_for_team_number)


@router.message(Registration.waiting_for_team_number)
async def process_team_number(message: Message, state: FSMContext):
    # Сохранить номер команды
    await state.update_data(team_number=message.text)

    # Запросить номер роли
    await message.answer("Введите номер вашей роли:")
    await state.set_state(Registration.waiting_for_role_number)


@router.message(Registration.waiting_for_role_number)
async def process_role_number(message: Message, state: FSMContext):
    # Сохранить номер роли
    await state.update_data(role_number=message.text)

    # Запросить номер уровня
    await message.answer("Введите номер вашего уровня:")
    await state.set_state(Registration.waiting_for_level_number)


@router.message(Registration.waiting_for_level_number)
async def process_level_number(message: Message, state: FSMContext):
    # Сохранить номер уровня
    await state.update_data(level_number=message.text)

    # Запросить описание деятельности
    await message.answer("Опишите, чем вы занимаетесь:")
    await state.set_state(Registration.waiting_for_activity_description)


@router.message(Registration.waiting_for_activity_description)
async def process_activity_description(message: Message, state: FSMContext):
    # Сохранить описание деятельности
    await state.update_data(activity_description=message.text)

    # Теперь можно сохранить все данные в базе данных
    user_data = await state.get_data()

    async for db in get_db():
        await add_user(
            db,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=user_data['full_name'],
            sber_id=user_data['sber_id'],
            comand_id=user_data['team_number'],
            role_id=user_data['role_number'],
            level_id=user_data['level_number'],
            description=user_data['activity_description'],
            # xor_encrypt_decrypt(telegram_name, TELEGRAM_TOKEN),
            # xor_encrypt_decrypt(full_name, TELEGRAM_TOKEN),
        )

    try:
        # Попытка сгенерировать временную ссылку на чат
        invite_link = await create_invite_link(message.bot, "-4571504763")
        await message.answer(
            "Регистрация завершена.\n"
            f"Вы зарегистрированы как: {user_data['full_name']}\n"
            f"Вот ссылка для вступления в группу: {invite_link}"
        )
    except TelegramBadRequest as error_rights:
        # Обработка ошибки, если недостаточно прав для создания ссылки
        await message.answer(
            "Не удалось создать ссылку приглашения. "
            "Недостаточно прав для управления приглашениями."
            f"Ошибка создания ссылки приглашения: {error_rights}"
        )
    await state.clear()


# Обработчик для кнопки "Продолжить"
@router.message(F.text == "Продолжить")
async def login(message: Message):
    telegram_id = message.from_user.id
    await message.answer(
        f"Пользователь ID: {telegram_id} нажал кнопку Продолжить"
    )


# Обработчик команды /get_user_info
@router.message(Command("get_user_info"))
async def get_user_info(message: Message):
    chat_id = message.chat.id
    telegram_id = message.from_user.id
    member = await message.bot.get_chat_member(chat_id, telegram_id)

    user_info = (
        f"Chat ID: {chat_id}\n"
        f"Имя: {member.user.full_name}\n"
        f"Username: @{member.user.username}\n"
        f"ID пользователя: {member.user.id}\n"
        f"Статус в чате: {member.status}"
    )

    await message.answer(user_info)


@router.message(Command("get_user_list"))
async def print_users_with_pagination(message: Message):
    async with SessionLocal() as session:
        users = await get_all_users(session, page=1, page_size=10)
        for user in users:
            all_users = "\n".join([
                f"User ID: {user.id}\n"
                f"Telegram ID: {user.telegram_id}\n"
                f"Telegram Name: {xor_encrypt_decrypt(user.username, TELEGRAM_TOKEN)}\n"
                f"Full Name: {xor_encrypt_decrypt(user.full_name, TELEGRAM_TOKEN)}\n"
            ])
            await message.answer(all_users)
