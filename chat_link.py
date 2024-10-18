import time
from aiogram.types import ChatInviteLink


# Функция для создания временной ссылки на приглашение в группу
async def create_invite_link(bot, chat_id):
    invite_link: ChatInviteLink = await bot.create_chat_invite_link(
        chat_id=chat_id,
        expire_date=int(time.time()) + 86400,  # Ссылка активна 24 часа
        member_limit=1  # Лимит на одного пользователя
    )
    return invite_link.invite_link
