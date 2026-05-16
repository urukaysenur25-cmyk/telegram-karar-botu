import sqlite3
from collections import Counter

async def admin_panel(update, context, ADMIN_ID):

    if update.effective_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # 👥 Toplam kullanıcı
    cursor.execute("""

    SELECT COUNT(*)
    FROM users

    """)

    toplam_kullanici = cursor.fetchone()[0]

    # 📊 Toplam kullanım
    cursor.execute("""

    SELECT SUM(kullanim)
    FROM users

    """)

    toplam_kullanim = cursor.fetchone()[0]

    if toplam_kullanim is None:
        toplam_kullanim = 0

    # ⭐ Favorisi olan kullanıcı
    cursor.execute("""

    SELECT COUNT(*)
    FROM users

    WHERE favori IS NOT NULL

    """)

    favorisi_olan = cursor.fetchone()[0]

    # 🧑 Kullanıcılar
    cursor.execute("""

    SELECT isim
    FROM users

    """)

    users = cursor.fetchall()

    kullanici_listesi = []

    for user in users:
        kullanici_listesi.append(f"• {user[0]}")

    kullanicilar = "\n".join(kullanici_listesi)

    # 🏆 En aktif kullanıcı
    cursor.execute("""

    SELECT isim, kullanim
    FROM users

    ORDER BY kullanim DESC
    LIMIT 1

    """)

    aktif = cursor.fetchone()

    if aktif:
        en_aktif_isim = aktif[0]
        en_aktif_kullanim = aktif[1]

    else:
        en_aktif_isim = "Yok"
        en_aktif_kullanim = 0

    # 🕒 Son aktif kullanıcılar
    cursor.execute("""

    SELECT isim, son_giris
    FROM users

    """)

    aktifler = cursor.fetchall()

    son_aktif = ""

    for user in aktifler:

        isim = user[0]
        tarih = user[1]

        son_aktif += f"• {isim} → {tarih}\n"

    # 🍔 En popüler yemek
    cursor.execute("""

    SELECT favori
    FROM users

    WHERE favori IS NOT NULL

    """)

    yemekler = cursor.fetchall()

    favoriler = []

    for yemek in yemekler:
        favoriler.append(yemek[0])

    if favoriler:

        sayac = Counter(favoriler)

        populer_yemek = sayac.most_common(1)[0][0]

    else:
        populer_yemek = "Yok"

    conn.close()

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