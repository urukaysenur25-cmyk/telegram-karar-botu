import json
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

    try:
        with open("data/users.json", "r", encoding="utf-8") as f:
            data = json.load(f)

    except:
        data = {}

    # 👤 kullanıcı yoksa oluştur
    if user_id not in data:

        data[user_id] = {
            "isim": query.from_user.first_name,
            "kullanim": 1,
            "favori": yemek
        }

    else:
        data[user_id]["favori"] = yemek

    with open("data/users.json", "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    await query.message.reply_text(
        f"Favorin kaydedildi: {yemek}",
        reply_markup=geri_btn()
    )

# 📋 FAVORİ GÖSTER
async def favori_goster(query, user_id):

    try:
        with open("data/users.json", "r", encoding="utf-8") as f:
            data = json.load(f)

    except:
        data = {}

    if user_id not in data:

        await query.message.reply_text(
            "Henüz favorin yok ❌",
            reply_markup=geri_btn()
        )

        return

    fav = data[user_id].get("favori")

    if fav:

        await query.message.reply_text(
            f"Favorin: {fav}",
            reply_markup=geri_btn()
        )

    else:

        await query.message.reply_text(
            "Henüz favorin yok ❌",
            reply_markup=geri_btn()
        )