import sqlite3
import random

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from utils.buttons import geri_btn

# 🍔 YEMEK ÖNER
async def yemek_oner(query):

    yemekler = [
        "Pizza 🍕",
        "Hamburger 🍔",
        "Döner 🌯",
        "Kebap 🍢",
        "Makarna 🍝",
        "Lahmacun 🫓",
        "Pide 🥙",
        "Tavuk Pilav 🍗",
        "Köfte 🍖",
        "Balık 🐟"
    ]

    secilen = random.choice(yemekler)

    keyboard = [
        [InlineKeyboardButton(
            "⭐ Favoriye ekle",
            callback_data=f"fav_{secilen}"
        )],
        [InlineKeyboardButton(
            "⬅️ Geri",
            callback_data="geri"
        )]
    ]

    await query.message.reply_text(
        secilen,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ⭐ FAVORİ KAYDET
async def favori_kaydet(query, user_id):

    yemek = query.data.replace("fav_", "")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""

    UPDATE users

    SET favori = ?

    WHERE user_id = ?

    """, (
        yemek,
        user_id
    ))

    conn.commit()
    conn.close()

    await query.message.reply_text(
        f"Favorin kaydedildi: {yemek}",
        reply_markup=geri_btn()
    )

# 📋 FAVORİ GÖSTER
async def favori_goster(query, user_id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""

    SELECT favori
    FROM users

    WHERE user_id = ?

    """, (user_id,))

    sonuc = cursor.fetchone()

    conn.close()

    if sonuc and sonuc[0]:

        await query.message.reply_text(
            f"Favorin: {sonuc[0]}",
            reply_markup=geri_btn()
        )

    else:

        await query.message.reply_text(
            "Henüz favorin yok ❌",
            reply_markup=geri_btn()
        )