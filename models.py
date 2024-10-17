import os

from dotenv import load_dotenv
from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.future import select

load_dotenv()
# URL подключения к SQLite базе данных
DATABASE_URL = os.environ['DATABASE_URL']
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Настройка сессии для работы с базой данных
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Определение базовой модели
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id: int = Column(BigInteger, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_user(
    db: AsyncSession,
    telegram_id:int,
    username: str,
    full_name: str
    ):

    new_user = User(
        telegram_id=telegram_id,
        username=username,
        full_name=full_name
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_all_users(db: AsyncSession, page: int, page_size: int = 10):
    # Вычисляем количество записей, которые нужно пропустить
    offset_value = (page - 1) * page_size
    # Выполняем запрос для получения всех записей из таблицы пользователей
    result = await db.execute(select(User).limit(page_size).offset(offset_value))
    # Преобразуем результат в список объектов
    return result.scalars().all()
