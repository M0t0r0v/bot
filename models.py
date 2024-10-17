import os

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

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
    username = Column(String, unique=True, index=True)
    full_name = Column(String)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_user(db: AsyncSession, username: str, full_name):
    new_user = User(username=username,
                    full_name=full_name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
