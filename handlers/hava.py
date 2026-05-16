import requests
from utils.buttons import geri_btn

async def hava_mesaj(update, context, API_KEY):

    text = update.message.text

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={text}&appid={API_KEY}&units=metric&lang=tr"
    )

    try:
        data = requests.get(url).json()

        await update.message.reply_text(
            f"{text} için hava:\n"
            f"🌡️ {data['main']['temp']}°C\n"
            f"☁️ {data['weather'][0]['description']}",
            reply_markup=geri_btn()
        )

    except:
        await update.message.reply_text(
            "Şehir bulunamadı ❌",
            reply_markup=geri_btn()
        )
        