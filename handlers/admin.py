async def admin_panel(update, context, ADMIN_ID, kullanici_sayisi):

    if update.effective_user.id != ADMIN_ID:
        return

    toplam = kullanici_sayisi()

    await update.message.reply_text(
        f"👑 Admin Panel\n\nToplam kullanıcı: {toplam}"
    )