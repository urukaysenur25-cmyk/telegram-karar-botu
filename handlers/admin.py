import json
from collections import Counter

async def admin_panel(update, context, ADMIN_ID):

    if update.effective_user.id != ADMIN_ID:
        return

    try:
        with open("data/users.json", "r", encoding="utf-8") as f:
            data = json.load(f)

    except:
        data = {}

    toplam_kullanici = len(data)

    toplam_kullanim = 0
    favorisi_olan = 0

    kullanici_listesi = []

    en_aktif_isim = "Yok"
    en_aktif_kullanim = 0

    son_aktif = ""

    favoriler = []

    for user in data.values():

        kullanim = user.get("kullanim", 0)

        toplam_kullanim += kullanim

        favori = user.get("favori")

        if favori:
            favorisi_olan += 1
            favoriler.append(favori)

        isim = user.get("isim", "Bilinmiyor")

        kullanici_listesi.append(
            f"• {isim}"
        )

        # 🏆 EN AKTİF KULLANICI
        if kullanim > en_aktif_kullanim:
            en_aktif_kullanim = kullanim
            en_aktif_isim = isim

        # 🕒 SON GİRİŞ
        tarih = user.get("son_giris", "Yok")

        son_aktif += f"• {isim} → {tarih}\n"

    kullanicilar = "\n".join(kullanici_listesi)

    # 🍔 EN POPÜLER YEMEK
    if favoriler:

        sayac = Counter(favoriler)

        populer_yemek = sayac.most_common(1)[0][0]

    else:
        populer_yemek = "Yok"

    mesaj = (
        f"👑 Admin Panel\n\n"
        f"👥 Toplam kullanıcı: {toplam_kullanici}\n"
        f"📊 Toplam kullanım: {toplam_kullanim}\n"
        f"⭐ Favorisi olan kullanıcı: {favorisi_olan}\n\n"
        f"🍔 En popüler yemek:\n"
        f"• {populer_yemek}\n\n"
        f"🏆 En aktif kullanıcı:\n"
        f"• {en_aktif_isim} ({en_aktif_kullanim} kullanım)\n\n"
        f"🕒 Son Aktif Kullanıcılar:\n"
        f"{son_aktif}\n"
        f"🧑 Kullanıcılar:\n{kullanicilar}"
    )

    await update.message.reply_text(mesaj)