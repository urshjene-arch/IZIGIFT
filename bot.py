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
        "🎁 <b>NFT Gift Watcher</b>\n\n"
        "✅ Ты подписан!\n"
        "🔎 Монитор запущен.",
        parse_mode="HTML"
    )


@dp.message(Command("test"))
async def test(message: Message):
    await message.answer(
        "🎁 <b>NFT GIFT UPGRADED!</b>\n\n"
        "👤 <a href=\"tg://user?id=123456789\">@test_user</a>\n"
        "🎁 Test Gift\n"
        "🔢 #123456\n"
        "🎨 Golden\n"
        "⭐ Star\n"
        "🌈 Purple",
        parse_mode="HTML"
    )


@telegram_client.on(events.NewMessage)
async def telegram_event(event):
    print("📨 Получено событие Telegram")


async def run_bot():
    print("🤖 Bot started")
    await dp.start_polling(bot)


async def run_monitor():
    print("🔎 NFT monitor starting")

    await telegram_client.connect()

    if not await telegram_client.is_user_authorized():
        print("❌ TELEGRAM_SESSION не авторизован")
        return

    print("✅ Telegram account authorized")

    await telegram_client.run_until_disconnected()


async def main():
    await asyncio.gather(
        run_bot(),
        run_monitor()
    )


if __name__ == "__main__":
    asyncio.run(main())
