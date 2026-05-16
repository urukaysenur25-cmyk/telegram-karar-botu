from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# 📋 ANA MENÜ
def ana_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🧠 Karar Veremiyorum!", callback_data="karar")],
        [InlineKeyboardButton("🎯 Bana Bir Şey Öner", callback_data="rastgele")],
        [InlineKeyboardButton("⚖️ İki Seçenek Arasında Kaldım", callback_data="secim")],
        [InlineKeyboardButton("🍔 Bugün Ne Yesem?", callback_data="yemek")],
        [InlineKeyboardButton("⭐ Favori Yemeğim", callback_data="favori_goster")],
        [InlineKeyboardButton("🌍 Hava Durumuna Bak", callback_data="hava")],
        [InlineKeyboardButton("🎲 Sürpriz Karar", callback_data="surpriz")],
        [InlineKeyboardButton("🧠 AI Tavsiye", callback_data="ai")]
    ])

# ⬅️ GERİ
def geri_btn():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Geri", callback_data="geri")]
    ])