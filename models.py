import os

from dotenv import load_dotenv
from sqlalchemy import BigInteger, Column, Integer, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
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
    # Инкрементный ключ
    id = Column(Integer, primary_key=True, index=True)
    # получаем от бота telegram_id
    telegram_id = Column(BigInteger, unique=True, index=True)
    # telegram_username получаем от бота
    username = Column(String, unique=True, index=True)
    # ФИО получаем от пользователя в telegram
    full_name = Column(String)
    # SberID получаем от пользователя в telegram
    sber_id = Column(String)
    # Внешний ключ на команду
    comand_id = Column(Integer, ForeignKey("command.id"))
    # Внешний ключ на роль
    role_id = Column(Integer, ForeignKey("role.id"))
    # Внешний ключ на уровень
    level_id = Column(Integer, ForeignKey("level.id"))
    # В кратце описание над чем работает человек
    description = Column(String)
    
    # Определяем отношения с другими таблицами
    comand = relationship("Comand")
    role = relationship("Role")
    level = relationship("Level")
    
    
class Comand(Base):
    __tablename__ = "command"
    id = Column(Integer, primary_key=True, index=True)
    comand_name = Column(String, unique=True)

class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, unique=True)

class Level(Base):
    __tablename__ = "level"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, unique=True) 


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

async def get_user_registered(db: AsyncSession, telegram_id:int) -> bool:
    # Выполняем запрос для получения информации по пользователю
    result = await db.execute(select(User).filter_by(telegram_id=telegram_id))
    # Преобразуем результат в список объектов
    user = result.scalar_one_or_none()
    return user is not None