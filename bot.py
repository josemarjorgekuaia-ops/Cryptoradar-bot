import os
import asyncio
import json
import websockets
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise ValueError("TOKEN ou CHAT_ID não configurados.")

bot = Bot(token=TOKEN)

SYMBOL = "btcusdt"  # Bitcoin em tempo real

async def run():
    url = f"wss://stream.binance.com:9443/ws/{SYMBOL}@trade"

    bot.send_message(chat_id=CHAT_ID, text="🚀 Sistema Tempo Real Ativo!")

    async with websockets.connect(url) as websocket:
        while True:
            data = await websocket.recv()
            trade = json.loads(data)

            price = trade["p"]

            print("Preço:", price)

            # Envia alerta exemplo (você pode melhorar depois)
            if float(price) % 100 == 0:
                bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"📊 BTC Preço: ${price}"
                )

asyncio.run(run())
