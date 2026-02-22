import os
import time
import requests
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise ValueError("TOKEN ou CHAT_ID não configurados.")

bot = Bot(token=TOKEN)

COINS = ["bitcoin", "ethereum", "binancecoin"]
LAST_SIGNAL = {}

def get_price(coin):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": coin, "vs_currencies": "usd"}
    r = requests.get(url, params=params, timeout=10)
    return r.json()[coin]["usd"]

def get_rsi(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": "usd", "days": "14"}
    r = requests.get(url, params=params, timeout=10)
    prices = [p[1] for p in r.json()["prices"]]

    gains, losses = [], []

    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))

    avg_gain = sum(gains)/len(gains) if gains else 0
    avg_loss = sum(losses)/len(losses) if losses else 0

    if avg_loss == 0:
        return 100

    rs = avg_gain/avg_loss
    return 100 - (100/(1+rs))

bot.send_message(chat_id=CHAT_ID, text="🚀 Sistema Profissional Completo Ativo!")

while True:
    try:
        for coin in COINS:
            price = get_price(coin)
            rsi = get_rsi(coin)

            signal = None

            if rsi < 30:
                signal = "COMPRA 🟢"
            elif rsi > 70:
                signal = "VENDA 🔴"

            # Anti-spam: só envia se mudar sinal
            if signal and LAST_SIGNAL.get(coin) != signal:
                bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"📊 {coin.upper()}\nPreço: ${price}\nRSI: {round(rsi,2)}\nSinal: {signal}"
                )
                LAST_SIGNAL[coin] = signal

        time.sleep(300)

    except Exception as e:
        print("Erro:", e)
        time.sleep(60)
