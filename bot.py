import os
import time
import requests
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

def get_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["bitcoin"]["usd"]

# Loop infinito (mantém o bot online)
while True:
    try:
        price = get_price()

        if price > 65000:
            bot.send_message(chat_id=CHAT_ID, text=f"🚀 SINAL DE COMPRA\nPreço: {price}")

        time.sleep(300)  # espera 5 minutos

    except Exception as e:
        print("Erro:", e)
        time.sleep(60)
