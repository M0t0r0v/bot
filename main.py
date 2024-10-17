import asyncio
from bot import bot, dp
from handlers import router
from aiogram.methods.delete_webhook import DeleteWebhook

from models import init_db


async def main():
    # Регистрируем роутеры
    dp.include_router(router)

    async def on_start(dp):
        await init_db()

    # Чтобы бот не реагировал на обновления в телеграме пока был выключен
    await bot(DeleteWebhook(drop_pending_updates=True))

    # Запуск бота
    await dp.start_polling(bot, on_startup=on_start)

if __name__ == '__main__':
    asyncio.run(main())
