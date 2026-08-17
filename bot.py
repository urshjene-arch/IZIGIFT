import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

BOT_TOKEN = os.environ["BOT_TOKEN"]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🎁 NFT Gift Watcher запущен!\n\n"
        "Я буду сообщать о новых NFT-подарках и их улучшениях."
    )


async def main():
    print("Bot started!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
