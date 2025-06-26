import os
import json
import datetime
import requests
from telegram import Bot
from dotenv import load_dotenv

# Load env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
DATA_FILE = "users.json"
bot = Bot(token=TOKEN)

# Ambil kutipan dari API
def get_motivational_quote():
    try:
        res = requests.get("https://zenquotes.io/api/random")
        if res.status_code == 200:
            data = res.json()[0]
            return f"💬 *{data['q']}*\n— {data['a']}"
    except:
        return "💬 Tetap semangat hari ini! 🚀"

# Kirim pesan ke user sesuai jadwal
def send_reminders():
    now = datetime.datetime.now().strftime("%H:%M")
    try:
        with open(DATA_FILE, "r") as f:
            users = json.load(f)
    except:
        users = {}

    for uid, info in users.items():
        if info.get("remind_time") == now:
            name = info.get("name", "Teman")
            message = (
                f"⏰ Hai {name}! Waktunya belajar! 📚\n\n{get_motivational_quote()}"
            )
            try:
                bot.send_message(chat_id=uid, text=message, parse_mode="Markdown")
            except Exception as e:
                print(f"Gagal kirim ke {uid}: {e}")

if __name__ == "__main__":
    send_reminders()
