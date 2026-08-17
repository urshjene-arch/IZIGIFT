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
    message = event.message
    action = getattr(message, "action", None)

    if action is None:
        return

    # Проверяем, является ли событие collectible gift
    if action.__class__.__name__ != "MessageActionStarGiftUnique":
        return

    # Нам нужны именно апгрейды
    if not getattr(action, "upgrade", False):
        return

    gift = getattr(action, "gift", None)

    if gift is None:
        return

    print("🎁 NFT UPGRADE DETECTED!")

    # Основные данные NFT
    title = getattr(gift, "title", "Unknown")
    number = getattr(gift, "num", "Unknown")
    slug = getattr(gift, "slug", None)

    # Кто получил/владеет подарком
    owner = getattr(gift, "owner_id", None)

    print(f"🎁 Gift: {title}")
    print(f"🔢 Number: #{number}")
    print(f"🔗 Slug: {slug}")
    print(f"👤 Owner: {owner}")

    # Кто инициировал событие
    sender = getattr(action, "from_id", None)

    print(f"👤 From: {sender}")

    # Получаем информацию о пользователе
    user = None

    try:
        if sender:
            user = await telegram_client.get_entity(sender)
    except Exception as e:
        print("Не удалось получить пользователя:", e)

    if user:
        username = getattr(user, "username", None)
        first_name = getattr(user, "first_name", "") or ""
        last_name = getattr(user, "last_name", "") or ""

        full_name = f"{first_name} {last_name}".strip()

        print(f"👤 Username: @{username}" if username else "👤 Username: нет")
        print(f"👤 Name: {full_name}")

    # Ссылка на NFT
    gift_link = None

    if slug:
        gift_link = f"https://t.me/nft/{slug}"

    # Отправляем уведомление подписчикам
    for chat_id in subscribers:

        user_text = "Неизвестный пользователь"

        if user:
            if getattr(user, "username", None):
                username = user.username
                user_text = f'<a href="https://t.me/{username}">@{username}</a>'
            else:
                user_id = user.id
                user_text = (
                    f'<a href="tg://user?id={user_id}">'
                    f'{user.first_name or "Пользователь"}'
                    f'</a>'
                )

        text = (
            "🎁 <b>NFT GIFT UPGRADED!</b>\n\n"
            f"👤 <b>Кто:</b> {user_text}\n"
            f"🎁 <b>Подарок:</b> {title}\n"
            f"🔢 <b>NFT:</b> #{number}\n"
        )

        if gift_link:
            text += f'\n🔗 <a href="{gift_link}">Открыть NFT</a>'

        try:
            await bot.send_message(
                chat_id,
                text,
                parse_mode="HTML"
            )
        except Exception as e:
            print("Ошибка отправки:", e)


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
