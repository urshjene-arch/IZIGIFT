import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

BOT_TOKEN = os.environ["BOT_TOKEN"]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

subscribers = set()


@dp.message(CommandStart())
async def start(message: Message):
    subscribers.add(message.chat.id)

    await message.answer(
        "🎁 NFT Gift Watcher\n\n"
        "✅ Ты подписан на уведомления!\n\n"
        "Когда монитор обнаружит апгрейд NFT-подарка, "
        "я отправлю уведомление сюда."
    )


@dp.message(Command("stop"))
async def stop(message: Message):
    subscribers.discard(message.chat.id)

    await message.answer(
        "🔕 Уведомления отключены."
    )


@dp.message(Command("test"))
async def test(message: Message):
    await send_upgrade_notification(
        chat_id=message.chat.id,
        gift_name="Test Gift",
        number=123456,
        model="Golden Model",
        symbol="⭐",
        backdrop="Purple"
    )


async def send_upgrade_notification(
    chat_id,
    gift_name,
    number,
    model,
    symbol,
    backdrop
):
    text = (
        "🎁 <b>NFT GIFT УЛУЧШЕН!</b>\n\n"
        f"🎁 Подарок: <b>{gift_name}</b>\n"
        f"🔢 NFT: <b>#{number}</b>\n"
        f"🎨 Модель: {model}\n"
        f"✨ Символ: {symbol}\n"
        f"🌈 Фон: {backdrop}\n"
    )

    await bot.send_message(
        chat_id,
        text,
        parse_mode="HTML"
    )


async def main():
    print("NFT Gift Watcher started!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
