# Telegram Digest Bot

A Python bot that fetches the last 24 hours of posts from a list of Telegram channels, summarizes each channel using Claude AI (Sonnet) with priority-based categorization, and sends the formatted digest to a Telegram chat via bot. Summaries are ordered by priority (high/medium/low) and kept in the original language of the posts. The bot tracks API costs per run and per month against a configurable budget.

## Setup

1. Create a virtual environment and install dependencies:
   ```
   python3 -m venv venv
   venv/bin/pip install -r requirements.txt
   ```

2. Copy `.env.example` or create a `.env` file with the following variables:
   ```
   TELEGRAM_API_ID=<your Telegram API ID from my.telegram.org>
   TELEGRAM_API_HASH=<your Telegram API hash>
   TELEGRAM_PHONE=<your phone number with country code>
   ANTHROPIC_API_KEY=<your Anthropic API key>
   TELEGRAM_BOT_TOKEN=<your Telegram bot token from @BotFather>
   TELEGRAM_CHAT_ID=<chat ID to send the digest to>
   ```

3. Edit `channels.json` to configure which channels to include.

## Run

```
venv/bin/python3 main.py
```

On first run, Telethon will ask for a verification code sent to your Telegram account.
