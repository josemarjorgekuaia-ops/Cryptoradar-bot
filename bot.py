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
LAST_SIGNAL = None

def get_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {"vs_currency": "usd", "days": "60"}
        r = requests.get(url, params=params, timeout=10)
        data = r.json().get("prices", [])
        prices = [p[1] for p in data]
        return prices
    except:
        return None

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

def load_or_train():
    prices = get_data()
    if prices is None or len(prices) < 20:
        return None

    if os.path.exists(MODEL_FILE):
        return joblib.load(MODEL_FILE)
    else:
        return train_model(prices)

model = load_or_train()

if model is None:
    raise Exception("Erro ao carregar modelo.")

bot.send_message(chat_id=CHAT_ID, text="🧠 IA Profissional Ativada!")

last_retrain = time.time()

while True:
    try:
        prices = get_data()
        if prices is None or len(prices) < 10:
            time.sleep(60)
            continue

        latest = prices[-10:]
        prediction = model.predict([latest])[0]

        signal = "ALTA 🚀" if prediction == 1 else "QUEDA 🔻"

        global LAST_SIGNAL
        if signal != LAST_SIGNAL:
            bot.send_message(chat_id=CHAT_ID, text=f"📊 IA prevê {signal}")
            LAST_SIGNAL = signal

        # Re-treina a cada 6 horas
        if time.time() - last_retrain > 21600:
            model = train_model(prices)
            last_retrain = time.time()
            bot.send_message(chat_id=CHAT_ID, text="🔄 IA re-treinada automaticamente")

        time.sleep(300)

    except Exception as e:
        print("Erro:", e)
        time.sleep(60)
