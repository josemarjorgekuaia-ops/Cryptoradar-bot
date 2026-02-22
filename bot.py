import os
import time
import requests
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

while True:
    price = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids":"bitcoin","vs_currencies":"usd"}
    ).json()["bitcoin"]["usd"]
    
    bot.send_message(
        chat_id=CHAT_ID,
        text=f"🚀 Bitcoin Price Now: ${price}"
    )
    
    time.sleep(300)  # espera 5 minutos
