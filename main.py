import asyncio
from bot import bot, dp
from handlers import router
from aiogram.methods.delete_webhook import DeleteWebhook


async def main():
    # Регистрируем роутеры
    dp.include_router(router)

    # Чтобы бот не реагировал на обновления в телеграме пока был выключен
    await bot(DeleteWebhook(drop_pending_updates=True))

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
