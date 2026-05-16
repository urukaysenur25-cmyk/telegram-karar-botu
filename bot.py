import os
import requests
import random
import sqlite3

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

    user_id = str(user.id)
    isim = user.first_name

    tarih = datetime.now().strftime("%d.%m.%Y %H:%M")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users (

        user_id TEXT PRIMARY KEY,
        isim TEXT,
        kullanim INTEGER,
        favori TEXT,
        son_giris TEXT

    )

    """)

    cursor.execute("""

    SELECT * FROM users
    WHERE user_id = ?

    """, (user_id,))

    mevcut = cursor.fetchone()

    if mevcut is None:

        cursor.execute("""

        INSERT INTO users
        (user_id, isim, kullanim, favori, son_giris)

        VALUES (?, ?, ?, ?, ?)

        """, (
            user_id,
            isim,
            1,
            None,
            tarih
        ))

    else:

        kullanim = mevcut[2] + 1

        cursor.execute("""

        UPDATE users

        SET kullanim = ?,
            son_giris = ?

        WHERE user_id = ?

        """, (
            kullanim,
            tarih,
            user_id
        ))

    conn.commit()
    conn.close()

# 📊 KULLANICI SAYISI
def kullanici_sayisi():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""

    SELECT COUNT(*)
    FROM users

    """)

    toplam = cursor.fetchone()[0]

    conn.close()

    return toplam

# 🆔 ID
async def id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        f"Senin ID: {update.effective_user.id}"
    )

# 👤 PROFİL SİSTEMİ
async def profil(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""

    SELECT isim, kullanim, favori, son_giris
    FROM users

    WHERE user_id = ?

    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    if not user:

        await update.message.reply_text(
            "Profil bulunamadı ❌"
        )

        return

    isim = user[0]
    kullanim = user[1]
    favori = user[2]
    son_giris = user[3]

    if favori is None:
        favori = "Yok"

    mesaj = (
        f"👤 Profilin\n\n"
        f"🧑 İsim: {isim}\n"
        f"📈 Kullanım: {kullanim}\n"
        f"⭐ Favori yemek: {favori}\n"
        f"🕒 Son giriş: {son_giris}"
    )

    await update.message.reply_text(mesaj)

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

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""

    SELECT user_id
    FROM users

    """)

    users = cursor.fetchall()

    conn.close()

    basarili = 0

    for user in users:

        try:

            await context.bot.send_message(
                chat_id=int(user[0]),
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

    # 🌍 HAVA
    elif query.data == "hava":

        await query.message.reply_text(
            "Şehir yaz (örnek: Istanbul)",
            reply_markup=geri_btn()
        )

        context.user_data["mod"] = "hava"

    # 🎲 SÜRPRİZ
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
        ADMIN_ID
    )

# ▶️ BOT
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CommandHandler("id", id))
app.add_handler(CommandHandler("profil", profil))
app.add_handler(CommandHandler("duyuru", duyuru))

app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj))

app.run_polling()