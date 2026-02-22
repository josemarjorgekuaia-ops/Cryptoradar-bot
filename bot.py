import os
from telegram import Bot

# Pega as variáveis do Render
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Cria o bot
bot = Bot(token=TOKEN)

# Envia mensagem automática
bot.send_message(
    chat_id=CHAT_ID,
    text="🚀 CryptoRadar está online e funcionando!"
)

print("Mensagem enviada com sucesso.")
