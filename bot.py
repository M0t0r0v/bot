import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from models import SessionLocal


load_dotenv()

TELEGRAM_TOKEN: str = os.getenv('TELEGRAM_TOKEN')

bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()  # Хранилище для состояний пользователей
dp = Dispatcher(storage=storage)


async def get_db():
    async with SessionLocal() as session:
        yield session  # Создаём сессию
