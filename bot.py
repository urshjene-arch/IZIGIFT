import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from telethon import TelegramClient, events
from telethon.sessions import StringSession


BOT_TOKEN = os.environ["BOT_TOKEN"]
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
TELEGRAM_SESSION = os.environ["TELEGRAM_SESSION"]


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

telegram_client = TelegramClient(
    StringSession(TELEGRAM_SESSION),
    API_ID,
    API_HASH
)

subscribers = set()


@dp.message(CommandStart())
async def start(message: Message):
    subscribers.add(message.chat.id)

    await message.answer(
        "🎁 NFT Gift Watcher\n\n"
        "✅ Бот работает!\n"
        "🔎 NFT монитор подключен."
    )


@dp.message(Command("test"))
async def test(message: Message):
    await message.answer(
        "🎁 NFT GIFT UPGRADED!\n\n"
        "👤 @test_user\n"
        "🎁 Test Gift\n"
        "🔢 #123456"
    )


@telegram_client.on(events.NewMessage)
async def telegram_event(event):
    print("📨 Получено событие Telegram")


async def run_bot():
    print("🤖 Bot started")

    try:
        await dp.start_polling(bot)

    except Exception as e:
        print("❌❌❌ BOT ERROR ❌❌❌")
        print("TYPE:", type(e).__name__)
        print("ERROR:", str(e))
        raise


async def run_monitor():
    print("🔎 NFT monitor starting")

    try:
        await telegram_client.connect()

        if not await telegram_client.is_user_authorized():
            print("❌ Telegram session is NOT authorized")
            return

        print("✅ Telegram account authorized")

        await telegram_client.run_until_disconnected()

    except Exception as e:
        print("❌❌❌ MONITOR ERROR ❌❌❌")
        print("TYPE:", type(e).__name__)
        print("ERROR:", str(e))
        raise


async def main():
    await asyncio.gather(
        run_bot(),
        run_monitor()
    )


if __name__ == "__main__":
    asyncio.run(main())
