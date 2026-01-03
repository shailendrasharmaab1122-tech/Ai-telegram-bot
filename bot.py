# ==========================================
# AI Telegram Bot
# Developed by: Devansh Sharma
# GitHub: https://github.com/shailendrasharmaab1122-tech
# ==========================================

import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)
import openai

# -------- CONFIG --------
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# -------- COMMANDS --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello!\n\n"
        "Main ek AI Telegram Bot hoon 🤖\n"
        "Tum mujhse **Hindi, English ya Hinglish** me kuch bhi pooch sakte ho.\n\n"
        "Bas apna sawaal likho 🙂"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 AI Telegram Bot\n\n"
        "Developed by: Devansh Sharma\n"
        "GitHub:\n"
        "https://github.com/shailendrasharmaab1122-tech\n\n"
        "Supports Hindi • English • Hinglish"
    )

# -------- AI REPLY --------
async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI Telegram bot. "
                        "Always reply in the same language as the user. "
                        "Support Hindi, English, and Hinglish. "
                        "Be clear, friendly, and simple."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )

        reply_text = response.choices[0].message.content.strip()
        await update.message.reply_text(reply_text)

    except Exception as e:
        await update.message.reply_text(
            "⚠️ Abhi thoda issue aa gaya hai.\n"
            "Please thodi der baad try karo."
        )

# -------- MAIN --------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

    print("🤖 AI Telegram Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()