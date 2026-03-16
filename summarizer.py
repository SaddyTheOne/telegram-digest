import anthropic

import config

SYSTEM_PROMPT = """You are a news digest assistant. You summarize Telegram channel posts into a concise daily digest.

For each post, write a 1-2 sentence summary with a priority emoji:
🔴 High - AI, Ukraine news, economic and political topics
🟡 Medium - Games, entertainment, fun
⚪ Low - Everything else

Format each summarized post as:
{emoji} {summary}
🔗 {link}

Order posts within a channel by priority: 🔴 first, then 🟡, then ⚪.
If a post has no meaningful text content, skip it.
Keep summaries in the original language of the post."""


async def summarize_messages(channel_name: str, messages: list[dict]) -> tuple[str, dict]:
    parts = []
    for msg in messages:
        parts.append(f"[{msg['date']}] {msg['text']}\nLink: {msg['link']}")

    user_message = f"Channel: {channel_name}\n\nMessages:\n---\n" + "\n---\n".join(parts) + "\n---"

    client = anthropic.AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY)
    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    summary_text = response.content[0].text
    usage_dict = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }

    return summary_text, usage_dict
