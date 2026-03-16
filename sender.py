from telegram import Bot

import config

MAX_LENGTH = 4096


def _split_message(text: str) -> list[str]:
    if len(text) <= MAX_LENGTH:
        return [text]

    chunks = []
    while text:
        if len(text) <= MAX_LENGTH:
            chunks.append(text)
            break

        split_at = text.rfind("\n", 0, MAX_LENGTH)
        if split_at == -1:
            split_at = MAX_LENGTH

        chunks.append(text[:split_at])
        text = text[split_at:].lstrip("\n")

    return chunks


async def send_digest(text: str) -> None:
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    chunks = _split_message(text)

    for chunk in chunks:
        await bot.send_message(
            chat_id=config.TELEGRAM_CHAT_ID,
            text=chunk,
            parse_mode="HTML",
        )
