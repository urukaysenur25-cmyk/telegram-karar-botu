import json
import os
import requests
import random

from datetime import datetime
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
        with open(dosya, "w", encoding="utf-8") as f:
            json.dump({}, f)

    try:
        with open(dosya, "r", encoding="utf-8") as f:
            data = json.load(f)

    except:
        data = {}

    user_id = str(user.id)

    tarih = datetime.now().strftime("%d.%m.%Y %H:%M")

    if user_id not in data:

        data[user_id] = {
            "isim": user.first_name,
            "kullanim": 1,
            "favori": None,
            "son_giris": tarih
        }

    else:

        data[user_id]["kullanim"] += 1
        data[user_id]["son_giris"] = tarih

    with open(dosya, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

# 📊 KULLANICI SAYISI
def kullanici_sayisi():

    try:
        with open("data/users.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        return len(data)

    except:
        return 0

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

# 📢 DUYURU SİSTEMİ
async def duyuru(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    mesaj = " ".join(context.args)

    if not mesaj:

        await update.message.reply_text(
            "Kullanım:\n/duyuru mesaj"
        )

        return

    try:
        with open("data/users.json", "r", encoding="utf-8") as f:
            data = json.load(f)

    except:
        data = {}

    basarili = 0

    for user_id in data.keys():

        try:

            await context.bot.send_message(
                chat_id=int(user_id),
                text=f"📢 Duyuru:\n\n{mesaj}"
            )

            basarili += 1

        except:
            pass

    await update.message.reply_text(
        f"✅ Duyuru gönderildi.\n👥 Gönderilen kişi: {basarili}"
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

    # 🧠 AI TAVSİYE
    elif query.data == "ai":

        keyboard = [

            [InlineKeyboardButton(
                "😢 Mutsuzum",
                callback_data="ai_mutsuz"
            )],

            [InlineKeyboardButton(
                "😰 Stresliyim",
                callback_data="ai_stres"
            )],

            [InlineKeyboardButton(
                "😴 Yorgunum",
                callback_data="ai_yorgun"
            )],

            [InlineKeyboardButton(
                "😒 Sıkıldım",
                callback_data="ai_sikildim"
            )],

            [InlineKeyboardButton(
                "⚖️ Kararsızım",
                callback_data="ai_kararsiz"
            )],

            [InlineKeyboardButton(
                "😔 Yalnızım",
                callback_data="ai_yalniz"
            )],

            [InlineKeyboardButton(
                "📚 Sınav Stresim Var",
                callback_data="ai_sinav"
            )],

            [InlineKeyboardButton(
                "⬅️ Geri",
                callback_data="geri"
            )]
        ]

        await query.message.reply_text(
            "🧠 Nasıl hissediyorsun?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 😢 MUTSUZ
    elif query.data == "ai_mutsuz":

        cevap = random.choice([

            "💙 Sevdiğin bir müzik açıp kısa yürüyüş yapabilirsin.",
            "🎬 Sevdiğin bir filmi açmak moralini düzeltebilir.",
            "☕ Bir kahve molası iyi gelebilir 😄",
            "💬 Yakın bir arkadaşınla konuşmak seni rahatlatabilir.",
            "🌙 Bazen dinlenmek her şeyden daha önemlidir."

        ])

        await query.message.reply_text(
            cevap,
            reply_markup=geri_btn()
        )

    # 😰 STRES
    elif query.data == "ai_stres":

        cevap = random.choice([

            "📚 25 dakikalık çalışma + kısa mola sistemi deneyebilirsin.",
            "🧘 Derin nefes almak ve kısa mola vermek iyi gelebilir.",
            "☕ Kısa bir kahve molası stresini azaltabilir.",
            "🎧 Sakin müzik açıp biraz rahatlamayı deneyebilirsin.",
            "🌿 Kısa yürüyüş yapmak zihnini toparlayabilir."

        ])

        await query.message.reply_text(
            cevap,
            reply_markup=geri_btn()
        )

    # 😴 YORGUN
    elif query.data == "ai_yorgun":

        cevap = random.choice([

            "😴 Biraz uyumak sana iyi gelebilir.",
            "☕ Enerji toplamak için kısa mola verebilirsin.",
            "🛌 Dinlenmek bazen en doğru karardır 😄",
            "🎵 Rahatlatıcı müzik eşliğinde dinlenebilirsin."

        ])

        await query.message.reply_text(
            cevap,
            reply_markup=geri_btn()
        )

    # 😒 SIKILDIM
    elif query.data == "ai_sikildim":

        cevap = random.choice([

            "🎮 Yeni bir oyun deneyebilirsin.",
            "🎬 Film veya dizi izlemek iyi gelebilir.",
            "📚 Yeni bir şey öğrenmeyi deneyebilirsin.",
            "🚶 Dışarı çıkıp kısa yürüyüş yapabilirsin.",
            "🎨 Yeni bir hobi denemeye ne dersin?"

        ])

        await query.message.reply_text(
            cevap,
            reply_markup=geri_btn()
        )

    # ⚖️ KARARSIZ
    elif query.data == "ai_kararsiz":

        cevap = random.choice([

            "⚖️ İçinden gelen ilk seçeneği denemek bazen en iyisidir 😄",
            "🎯 Seni en mutlu edecek seçeneği düşün.",
            "💡 Çok düşünmek yerine küçük adımla başlamayı dene.",
            "🚀 Risk almak bazen güzel sonuçlar doğurabilir."

        ])

        await query.message.reply_text(
            cevap,
            reply_markup=geri_btn()
        )

    # 😔 YALNIZ
    elif query.data == "ai_yalniz":

        cevap = random.choice([

            "💬 Bir arkadaşınla konuşmak iyi hissettirebilir.",
            "📱 Sevdiğin biriyle mesajlaşmayı deneyebilirsin.",
            "🌿 Dışarı çıkıp biraz hava almak iyi gelebilir.",
            "🎵 Müzik bazen insanın en iyi arkadaşı olabilir."

        ])

        await query.message.reply_text(
            cevap,
            reply_markup=geri_btn()
        )

    # 📚 SINAV
    elif query.data == "ai_sinav":

        cevap = random.choice([

            "📚 Küçük hedeflerle çalışmak daha verimli olabilir.",
            "⏳ Pomodoro tekniğini deneyebilirsin.",
            "☕ Kısa mola sonrası çalışmak daha etkili olur.",
            "💪 Düzenli tekrar yapmak seni rahatlatır."

        ])

        await query.message.reply_text(
            cevap,
            reply_markup=geri_btn()
        )

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

# 👑 ADMIN
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await admin_panel(
        update,
        context,
        ADMIN_ID
    )

# ▶️ BOT
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CommandHandler("id", id))
app.add_handler(CommandHandler("duyuru", duyuru))

app.add_handler(CallbackQueryHandler(button))

app.run_polling()