import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path

from reader import fetch_messages
from summarizer import summarize_messages
from sender import send_digest
from cost_tracker import calculate_cost, record_cost, format_cost_line

CHANNELS_FILE = Path(__file__).parent / "channels.json"

UA_MONTHS = {
    1: "січня", 2: "лютого", 3: "березня", 4: "квітня",
    5: "травня", 6: "червня", 7: "липня", 8: "серпня",
    9: "вересня", 10: "жовтня", 11: "листопада", 12: "грудня",
}


async def main():
    yesterday = datetime.now() - timedelta(days=1)
    date_str = f"{yesterday.day} {UA_MONTHS[yesterday.month]} {yesterday.year}"

    channels = json.loads(CHANNELS_FILE.read_text())["channels"]
    digest_parts = [f"📅 Дайджест за {date_str}"]
    total_cost = 0.0

    for channel in channels:
        messages = await fetch_messages(channel)
        print(f"Fetched {len(messages)} messages from @{channel}")

        if not messages:
            continue

        summary, usage = await summarize_messages(channel, messages)
        cost = calculate_cost(usage)
        total_cost += cost
        print(f"  Summarized ({usage['input_tokens']}in/{usage['output_tokens']}out, ${cost:.4f})")

        digest_parts.append(f"📢 <b>{channel}</b>\n\n{summary}")

    if not digest_parts:
        print("No messages to summarize.")
        return

    data = record_cost(total_cost)
    cost_line = format_cost_line(total_cost, data)
    print(f"\n{cost_line}")

    digest_text = "\n\n".join(digest_parts) + "\n\n" + cost_line
    await send_digest(digest_text)
    print("Digest sent.")


if __name__ == "__main__":
    asyncio.run(main())
