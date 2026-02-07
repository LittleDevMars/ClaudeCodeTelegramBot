# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

A Telegram bot that forwards user messages to the Claude CLI and returns responses. Maintains per-chat conversation history with configurable limits.

## Setup & Running

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set TELEGRAM_BOT_TOKEN

# Run the bot
python bot.py
```

**Prerequisite**: The `claude` CLI must be installed and accessible in PATH.

## Architecture

Single-file bot (`bot.py`) with:
- **Conversation storage**: In-memory dict keyed by `chat_id`, stores `(user_message, assistant_response)` tuples
- **Claude integration**: Spawns `claude -p <prompt>` subprocess, includes conversation history in prompt
- **Message handling**: Splits long responses (>4096 chars) at newline boundaries for Telegram's limit

### Key Constants
- `MAX_MESSAGE_LENGTH = 4096` - Telegram message limit
- `MAX_HISTORY = 20` - Max conversation turns retained
- `MAX_HISTORY_CHARS = 10000` - Truncates older history beyond this

### Bot Commands
- `/start` - Welcome message
- `/reset` - Clears conversation history for current chat
