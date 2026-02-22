import os
import numpy as np
import requests
from telegram import Bot
from sklearn.ensemble import RandomForestClassifier

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise ValueError("TOKEN ou CHAT_ID não configurados.")

bot = Bot(token=TOKEN)

def get_price_history():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "30"}
    r = requests.get(url, params=params)
    prices = [p[1] for p in r.json()["prices"]]
    return prices

def train_model(prices):
    X = []
    y = []

    for i in range(5, len(prices)-1):
        features = prices[i-5:i]
        label = 1 if prices[i+1] > prices[i] else 0
        X.append(features)
        y.append(label)

    model = RandomForestClassifier()
    model.fit(X, y)
    return model

bot.send_message(chat_id=CHAT_ID, text="🧠 IA Profissional Iniciada!")

prices = get_price_history()
model = train_model(prices)

while True:
    latest = get_price_history()[-5:]
    prediction = model.predict([latest])[0]

    if prediction == 1:
        bot.send_message(chat_id=CHAT_ID, text="📈 IA prevê ALTA 🔵")
    else:
        bot.send_message(chat_id=CHAT_ID, text="📉 IA prevê QUEDA 🔴")

    import time
    time.sleep(300)
