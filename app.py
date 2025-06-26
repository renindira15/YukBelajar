import os
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Load env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
DATA_FILE = "users.json"

# Fungsi load & simpan data user
def load_users():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# /start command
def start(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)
    users = load_users()
    users[user_id] = {
        "remind_time": "07:00",
        "name": update.message.from_user.first_name
    }
    save_users(users)
    update.message.reply_text(
        "✅ Kamu berhasil terdaftar!\n"
        "Aku akan kirim pengingat belajar setiap jam 07:00 pagi.\n"
        "Kamu bisa ubah jadwal dengan perintah /set HH:MM"
    )

# /set command
def set_reminder(update: Update, context: CallbackContext):
    if len(context.args) != 1 or not context.args[0].count(":") == 1:
        update.message.reply_text("⚠️ Format salah. Contoh: /set 08:30")
        return
    time_str = context.args[0]
    user_id = str(update.message.chat_id)
    users = load_users()
    if user_id not in users:
        update.message.reply_text("❗Kamu belum terdaftar. Gunakan /start dulu.")
        return
    users[user_id]["remind_time"] = time_str
    save_users(users)
    update.message.reply_text(f"🔔 Jadwal pengingat diubah ke {time_str}")

# Setup bot
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("set", set_reminder))

# Jalankan bot
updater.start_polling()
updater.idle()
