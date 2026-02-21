import os
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

bot.send_message(chat_id=CHAT_ID, text="🚀 CryptoRadar está online!")
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "CryptoRadar online 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
