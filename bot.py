import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from telethon import TelegramClient, events
from telethon.tl.types import MessageActionStarGiftUnique
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


# =========================
# TELEGRAM BOT
# =========================

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


# =========================
# NFT UPGRADE MONITOR
# =========================

@telegram_client.on(events.Raw)
async def telegram_event(update):

    try:
        # Получаем сообщение из raw update
        message = getattr(update, "message", None)

        if not message:
            return

        # Получаем action сообщения
        action = getattr(message, "action", None)

        # Нас интересует только уникальный Gift после upgrade
        if not isinstance(action, MessageActionStarGiftUnique):
            return

        # Проверяем, что это именно upgrade
        if not getattr(action, "upgrade", False):
            return

        gift = getattr(action, "gift", None)

        print("\n" + "=" * 60)
        print("🚨 NFT GIFT UPGRADE!")
        print("=" * 60)

        print(
            "👤 Кто сделал upgrade:",
            getattr(action, "from_id", None)
        )

        print(
            "🎁 Gift:",
            getattr(gift, "title", None)
        )

        print(
            "🆔 NFT ID:",
            getattr(gift, "id", None)
        )

        print(
            "🔢 NFT номер:",
            getattr(gift, "num", None)
        )

        print(
            "🔗 Slug:",
            getattr(gift, "slug", None)
        )

        print(
            "📨 Message ID:",
            getattr(message, "id", None)
        )

        print("=" * 60)

    except Exception as e:

        print("\n❌ NFT EVENT ERROR")
        print("TYPE:", type(e).__name__)
        print("ERROR:", str(e))


# =========================
# BOT
# =========================

async def run_bot():

    print("🤖 Bot started")

    try:

        await dp.start_polling(bot)

    except Exception as e:

        print("❌❌❌ BOT ERROR ❌❌❌")
        print("TYPE:", type(e).__name__)
        print("ERROR:", str(e))

        raise


# =========================
# TELEGRAM ACCOUNT MONITOR
# =========================

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


# =========================
# MAIN
# =========================

async def main():

    await asyncio.gather(
        run_bot(),
        run_monitor()
    )


if __name__ == "__main__":

    asyncio.run(main())
