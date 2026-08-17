import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from telethon import TelegramClient, events


BOT_TOKEN = os.environ["BOT_TOKEN"]
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

telegram_client = TelegramClient(
    "nft_monitor",
    API_ID,
    API_HASH
)


subscribers = set()


@dp.message(CommandStart())
async def start(message: Message):
    subscribers.add(message.chat.id)

    await message.answer(
        "🎁 NFT Gift Watcher\n\n"
        "✅ Ты подписан на уведомления!"
    )


@dp.message()
async def messages(message: Message):
    if message.text == "/test":
        await send_test(message.chat.id)


async def send_test(chat_id):
    await bot.send_message(
        chat_id,
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
    text = event.message.text or ""

    if "gift" in text.lower() or "подар" in text.lower():
        print("🎁 Обнаружено сообщение о подарке:")
        print(text)


async def run_bot():
    print("🤖 Bot started")
    await dp.start_polling(bot)


async def run_monitor():
    print("🔎 NFT monitor starting")

    await telegram_client.start()

    print("✅ Telegram monitor connected")

    await telegram_client.run_until_disconnected()


async def main():
    await asyncio.gather(
        run_bot(),
        run_monitor()
    )


if __name__ == "__main__":
    asyncio.run(main())
