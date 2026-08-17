import os
from telethon import TelegramClient, events

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

client = TelegramClient("nft_monitor", API_ID, API_HASH)


@client.on(events.NewMessage)
async def new_message(event):
    message = event.message

    # Пока просто ищем сообщения, связанные с подарками.
    text = message.text or ""

    if "gift" in text.lower() or "подар" in text.lower():
        print("🎁 Возможно обнаружен подарок:")
        print(text)

    # В следующем этапе сюда добавим
    # обработку реального messageActionStarGiftUnique.


async def main():
    print("🔎 NFT monitor started")
    await client.start()
    print("✅ Telegram account connected")
    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())
