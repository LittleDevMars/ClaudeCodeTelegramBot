import os
import asyncio
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 4096
MAX_HISTORY = 20
MAX_HISTORY_CHARS = 10000

# chat_id -> list of (user_message, assistant_response)
conversations: dict[int, list[tuple[str, str]]] = {}


async def ask_claude(chat_id: int, message: str) -> str:
    history = conversations.get(chat_id, [])

    prompt = ""
    if history:
        history_text = ""
        for user_msg, assistant_msg in history:
            history_text += f"User: {user_msg}\nAssistant: {assistant_msg}\n"
        if len(history_text) > MAX_HISTORY_CHARS:
            history_text = history_text[-MAX_HISTORY_CHARS:]
            history_text = history_text[history_text.find("\n") + 1:]
        prompt += f"Previous conversation:\n{history_text}\n"
    prompt += f"User: {message}"

    process = await asyncio.create_subprocess_exec(
        "claude", "-p", prompt,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        error_text = stderr.decode().strip()
        logger.error("claude CLI error (code %d): %s", process.returncode, error_text)
        return f"[Error from Claude CLI: {error_text}]"

    response = stdout.decode().strip()

    if response:
        if chat_id not in conversations:
            conversations[chat_id] = []
        conversations[chat_id].append((message, response))
        if len(conversations[chat_id]) > MAX_HISTORY:
            conversations[chat_id] = conversations[chat_id][-MAX_HISTORY:]

    return response


def split_message(text: str) -> list[str]:
    if len(text) <= MAX_MESSAGE_LENGTH:
        return [text]

    chunks = []
    while text:
        if len(text) <= MAX_MESSAGE_LENGTH:
            chunks.append(text)
            break

        split_pos = text.rfind("\n", 0, MAX_MESSAGE_LENGTH)
        if split_pos == -1:
            split_pos = MAX_MESSAGE_LENGTH

        chunks.append(text[:split_pos])
        text = text[split_pos:].lstrip("\n")

    return chunks


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "안녕하세요! 메시지를 보내주시면 Claude에게 전달해 드릴게요.\n"
        "/reset 으로 대화 기록을 초기화할 수 있습니다."
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    conversations.pop(chat_id, None)
    await update.message.reply_text("대화 기록이 초기화되었습니다.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    logger.info("Received message from user %s", update.effective_user.id)

    await update.message.chat.send_action("typing")

    response = await ask_claude(update.effective_chat.id, user_message)

    if not response:
        await update.message.reply_text("[Claude가 빈 응답을 반환했습니다]")
        return

    for chunk in split_message(response):
        await update.message.reply_text(chunk)


def main() -> None:
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN 환경변수가 설정되지 않았습니다")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
