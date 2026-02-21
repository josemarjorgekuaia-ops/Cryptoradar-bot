import os
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

bot.send_message(chat_id=CHAT_ID, text="🚀 CryptoRadar está online!")
