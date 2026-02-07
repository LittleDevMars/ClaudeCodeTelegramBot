#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    echo "Please copy .env.example to .env and configure TELEGRAM_BOT_TOKEN"
    exit 1
fi

# Check if claude CLI is installed
if ! command -v claude &> /dev/null; then
    echo "Error: claude CLI not found in PATH"
    echo "Please install claude CLI first"
    exit 1
fi

# Run the bot
echo "Starting Telegram bot..."
python bot.py
