import random
from utils.buttons import geri_btn

async def secim_yap(update, context):

    text = update.message.text

    try:
        a, b = text.split(",")

        await update.message.reply_text(
            f"Seçim: {random.choice([a.strip(), b.strip()])}",
            reply_markup=geri_btn()
        )

    except:
        await update.message.reply_text(
            "Doğru yazım: A,B",
            reply_markup=geri_btn()
        )