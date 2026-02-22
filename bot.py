import os
import time
import requests
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

def get_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}
    return requests.get(url, params=params).json()["bitcoin"]["usd"]

def get_rsi():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "14"}
    data = requests.get(url, params=params).json()
    prices = [p[1] for p in data["prices"]]

    gains = []
    losses = []

    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
        else:
            losses.append(abs(change))

    avg_gain = sum(gains) / len(gains) if gains else 0
    avg_loss = sum(losses) / len(losses) if losses else 0

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

while True:
    try:
        price = get_price()
        rsi = get_rsi()

        # Só envia sinal forte
        if rsi < 30:
            bot.send_message(
                chat_id=CHAT_ID,
                text=f"🟢 SINAL DE COMPRA\nPreço: ${price}\nRSI: {round(rsi,2)}"
            )

        elif rsi > 70:
            bot.send_message(
                chat_id=CHAT_ID,
                text=f"🔴 SINAL DE VENDA\nPreço: ${price}\nRSI: {round(rsi,2)}"
            )

        time.sleep(300)

    except Exception as e:
        print("Erro:", e)
        time.sleep(60)
