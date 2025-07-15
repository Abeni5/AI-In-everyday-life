import os
import json
import asyncio
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
DATA_PATH = "data/raw/telegram_messages"
IMG_PATH = "data/raw/images"
CHANNELS = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma"
]

os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(IMG_PATH, exist_ok=True)

async def scrape_channel(channel):
    date_str = datetime.now().strftime("%Y-%m-%d")
    save_path = os.path.join(DATA_PATH, f"{date_str}_{channel.split('/')[-1]}.json")

    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        messages_data = []

        async for message in client.iter_messages(channel, limit=100):
            data = {
                "id": message.id,
                "date": str(message.date),
                "text": message.text,
                "has_photo": isinstance(message.media, MessageMediaPhoto)
            }

            if isinstance(message.media, MessageMediaPhoto):
                photo_path = os.path.join(IMG_PATH, f"{channel.split('/')[-1]}_{message.id}.jpg")
                await message.download_media(photo_path)
                data["photo_path"] = photo_path

            messages_data.append(data)

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(messages_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Scraped {len(messages_data)} messages from {channel}")

if __name__ == "__main__":
    for ch in CHANNELS:
        asyncio.run(scrape_channel(ch))
