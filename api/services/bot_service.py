from bot.utils.utils import get_bot


bot = get_bot()


async def send_notify(chat_id: int, text: str):
    await bot.send_message(chat_id=chat_id, text=text)
