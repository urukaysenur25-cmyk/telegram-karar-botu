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

    with open("data/users.json", "r") as f:
        data = json.load(f)

    data[user_id]["favori"] = yemek

    with open("data/users.json", "w") as f:
        json.dump(data, f, indent=4)

    await query.message.reply_text(
        f"Favorin kaydedildi: {yemek}",
        reply_markup=geri_btn()
    )

# 📋 FAVORİ GÖSTER
async def favori_goster(query, user_id):

    with open("data/users.json", "r") as f:
        data = json.load(f)

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