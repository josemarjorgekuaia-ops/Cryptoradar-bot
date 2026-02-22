import os
import time
import numpy as np
import requests
import joblib
from telegram import Bot
from sklearn.neural_network import MLPClassifier

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise ValueError("TOKEN ou CHAT_ID não configurados.")

bot = Bot(token=TOKEN)

MODEL_FILE = "model.pkl"

def get_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "60"}
    r = requests.get(url, params=params)
    prices = [p[1] for p in r.json()["prices"]]
    return prices

def train_model(prices):
    X = []
    y = []

    for i in range(10, len(prices)-1):
        features = prices[i-10:i]
        label = 1 if prices[i+1] > prices[i] else 0
        X.append(features)
        y.append(label)

    model = MLPClassifier(hidden_layer_sizes=(50,50), max_iter=500)
    model.fit(X, y)
    joblib.dump(model, MODEL_FILE)
    return model

# Carregar ou treinar
if os.path.exists(MODEL_FILE):
    model = joblib.load(MODEL_FILE)
else:
    prices = get_data()
    model = train_model(prices)

bot.send_message(chat_id=CHAT_ID, text="🧠 IA Deep Learning Ativada!")

while True:
    prices = get_data()
    latest = prices[-10:]
    prediction = model.predict([latest])[0]

    if prediction == 1:
        bot.send_message(chat_id=CHAT_ID, text="📈 IA prevê ALTA 🚀")
    else:
        bot.send_message(chat_id=CHAT_ID, text="📉 IA prevê QUEDA 🔻")

    time.sleep(300)
