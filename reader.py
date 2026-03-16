from datetime import datetime, timezone, timedelta

from telethon import TelegramClient

import config


async def fetch_messages(channel_username: str, hours: int = 24) -> list[dict]:
    client = TelegramClient("digest", config.API_ID, config.API_HASH)
    await client.start(phone=config.PHONE)

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    messages: list[dict] = []

    async for msg in client.iter_messages(channel_username, offset_date=cutoff, reverse=True):
        if msg.date < cutoff:
            continue
        if not msg.text:
            continue
        messages.append({
            "id": msg.id,
            "text": msg.text,
            "date": msg.date,
            "link": f"https://t.me/{channel_username}/{msg.id}",
        })

    await client.disconnect()
    return messages
