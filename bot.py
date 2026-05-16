import json
import os
import requests
import random

from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

from utils.buttons import ana_menu, geri_btn
from handlers.hava import hava_mesaj
from handlers.karar import secim_yap
from handlers.admin import admin_panel
from handlers.yemek import (
    yemek_oner,
    favori_kaydet,
    favori_goster
)

load_dotenv()

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")

ADMIN_ID = 8547388845

# 👤 KULLANICI KAYDET
def kullanici_kaydet(user):
    dosya = "data/users.json"

    if not os.path.exists(dosya):
        with open(dosya, "w") as f:
            json.dump({}, f)

    with open(dosya, "r") as f:
        data = json.load(f)

    user_id = str(user.id)

    if user_id not in data:
        data[user_id] = {
            "isim": user.first_name,
            "kullanim": 1,
            "favori": None
        }
    else:
        data[user_id]["kullanim"] += 1

    with open(dosya, "w") as f:
      json.dump(data, f, indent=4, ensure_ascii=False)

# 📊 KULLANICI SAYISI
def kullanici_sayisi():
    with open("data/users.json", "r") as f:
        data = json.load(f)
        

    return len(data)

# 🆔 ID
async def id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Senin ID: {update.effective_user.id}"
    )

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kullanici_kaydet(update.effective_user)

    await update.message.reply_text(
        "Karar veremiyorsan yardımcı olayım 👇",
        reply_markup=ana_menu()
    )

# 🎮 BUTONLAR
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)

    if query.data == "geri":
        await query.message.reply_text(
            "Ana menü 👇",
            reply_markup=ana_menu()
        )

    elif query.data == "karar":
        keyboard = [
            [InlineKeyboardButton("😄 Mutluyum", callback_data="mutlu")],
            [InlineKeyboardButton("😴 Yorgunum", callback_data="yorgun")],
            [InlineKeyboardButton("😒 Sıkıldım", callback_data="sikildim")],
            [InlineKeyboardButton("⬅️ Geri", callback_data="geri")]
        ]

        await query.message.reply_text(
            "Nasıl hissediyorsun?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "mutlu":
        await query.message.reply_text(
            "Dışarı çıkıp eğlenebilirsin 🎉",
            reply_markup=geri_btn()
        )

    elif query.data == "yorgun":
        await query.message.reply_text(
            "Biraz dinlenmek iyi gelir 😌",
            reply_markup=geri_btn()
        )

    elif query.data == "sikildim":
        await query.message.reply_text(
            "Film izlemeye ne dersin 🎬",
            reply_markup=geri_btn()
        )

    elif query.data == "rastgele":
        secenekler = [
            "Ders çalış 📚",
            "Uyu 😄",
            "Film izle 🎬",
            "Dışarı çık 🌿"
        ]

        await query.message.reply_text(
            random.choice(secenekler),
            reply_markup=geri_btn()
        )

    elif query.data == "secim":
        await query.message.reply_text(
            "Şöyle yaz: A,B",
            reply_markup=geri_btn()
        )

        context.user_data["mod"] = "secim"

    # 🍔 YEMEK
    elif query.data == "yemek":

        await yemek_oner(query)

    # ⭐ FAVORİ KAYDET
    elif query.data.startswith("fav_"):

        await favori_kaydet(query, user_id)

    # 📋 FAVORİ GÖSTER
    elif query.data == "favori_goster":

        await favori_goster(query, user_id)

    elif query.data == "hava":
        await query.message.reply_text(
            "Şehir yaz (örnek: Istanbul)",
            reply_markup=geri_btn()
        )

        context.user_data["mod"] = "hava"

    elif query.data == "surpriz":
        secenekler = [
            "Yeni bir şey dene 🚀",
            "Müzik aç 🎧",
            "Arkadaşınla konuş 💬",
            "Yürüyüş yap 🚶"
        ]

        await query.message.reply_text(
            random.choice(secenekler),
            reply_markup=geri_btn()
        )

# 💬 MESAJ
async def mesaj(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # 🌍 HAVA
    if context.user_data.get("mod") == "hava":

        await hava_mesaj(update, context, API_KEY)

        context.user_data["mod"] = None

    # ⚖️ SEÇİM
    elif context.user_data.get("mod") == "secim":

        await secim_yap(update, context)

        context.user_data["mod"] = None

# 👑 ADMIN
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await admin_panel(
        update,
        context,
        ADMIN_ID,
        kullanici_sayisi
    )

# ▶️ BOT
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CommandHandler("id", id))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        mesaj
    )
)

app.run_polling()