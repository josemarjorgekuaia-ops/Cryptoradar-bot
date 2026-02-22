import os
import time
import requests
import numpy as np
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise ValueError("TOKEN ou CHAT_ID não configurados.")

bot = Bot(token=TOKEN)

ASSETS = {
    "BTC": "bitcoin",
    "ETH": "ethereum"
}

LAST_SIGNAL = {}

def get_market_data(coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {"vs_currency": "usd", "days": "30"}
        r = requests.get(url, params=params, timeout=10)
        prices = [p[1] for p in r.json()["prices"]]
        return prices
    except:
        return None

def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    gains = deltas[deltas > 0]
    losses = -deltas[deltas < 0]

    avg_gain = np.mean(gains) if len(gains) > 0 else 0
    avg_loss = np.mean(losses) if len(losses) > 0 else 0

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def detect_market_trend(prices):
    short_ma = np.mean(prices[-5:])
    long_ma = np.mean(prices[-20:])

    if short_ma > long_ma:
        return "Bull 🟢"
    elif short_ma < long_ma:
        return "Bear 🔴"
    else:
        return "Lateral ⚪"

bot.send_message(chat_id=CHAT_ID, text="🚀 Sistema Inteligente Ativado!")

while True:
    try:
        for symbol, coin_id in ASSETS.items():

            prices = get_market_data(coin_id)
            if prices is None or len(prices) < 20:
                continue

            rsi = calculate_rsi(prices)
            trend = detect_market_trend(prices)
            current_price = round(prices[-1], 2)

            signal = None

            if rsi < 30 and trend == "Bull 🟢":
                signal = "COMPRA 🟢"
            elif rsi > 70 and trend == "Bear 🔴":
                signal = "VENDA 🔴"

            if signal and LAST_SIGNAL.get(symbol) != signal:
                bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"""
📊 Ativo: {symbol}
Preço: ${current_price}
RSI: {round(rsi,2)}
Tendência: {trend}
Sinal: {signal}
"""
                )
                LAST_SIGNAL[symbol] = signal

        time.sleep(300)

    except Exception as e:
        print("Erro:", e)
        time.sleep(60)
