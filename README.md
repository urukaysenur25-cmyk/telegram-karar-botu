# 🤖 Telegram Karar Botu

Bu bot, kullanıcıların günlük hayatta karar vermesine yardımcı olmak için geliştirilmiştir.

---

## 🚀 Özellikler

* 🧠 Karar veremeyenler için öneriler
* 🎯 Rastgele aktivite seçimi
* ⚖️ İki seçenek arasında karar verme (A mı B mi)
* 🍔 Yemek önerisi
* ⭐ Favori yemek kaydetme sistemi
* 🌍 Hava durumu sorgulama
* 🎲 Sürpriz öneriler
* 👑 Admin paneli
* 📢 Duyuru sistemi
* 🧠 AI tavsiye sistemi

---

## 🛠️ Kullanılan Teknolojiler

* Python
* python-telegram-bot
* OpenWeather API
* JSON veri saklama
* python-dotenv

---

## 📦 Kurulum

Projeyi bilgisayarına indir:

```bash
git clone https://github.com/kullaniciadi/projeadi.git
cd projeadi
```

Gerekli kütüphaneleri yükle:

```bash
pip install -r requirements.txt
```

---

## 🔐 .env Dosyası

Proje klasörüne `.env` dosyası oluştur:

```env
TOKEN=YOUR_BOT_TOKEN
API_KEY=YOUR_API_KEY
```

---

## ▶️ Çalıştırma

```bash
python bot.py
```

---

## 📁 Proje Yapısı

```text
telegram_bot/
│
├── handlers/
│   ├── hava.py
│   ├── karar.py
│   ├── admin.py
│   ├── yemek.py
│
├── utils/
│   ├── buttons.py
│
├── data/
│   ├── users.json
│
├── screenshots/
│   ├── menu.jpeg
│   ├── hava.jpeg
│   ├── yemek.jpeg
│   ├── secim.jpeg
│   ├── admin.jpeg
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── bot.py
```

---

## 🔐 Güvenlik

Bu projede güvenlik nedeniyle:

* Telegram BOT TOKEN
* API KEY

gibi gizli bilgiler `.env` dosyasında tutulmaktadır.

---

## 👨‍💻 Geliştirici

Bu proje eğitim amaçlı geliştirilmiştir.

---

# 📸 Ekran Görüntüleri

## 🏠 Ana Menü

<img src="screenshots/menu.jpeg" width="250"/>

---

## 🌍 Hava Durumu

<img src="screenshots/hava.jpeg" width="250"/>

---

## 🍔 Yemek Önerisi

<img src="screenshots/yemek.jpeg" width="250"/>

---

## ⚖️ Seçim Sistemi

<img src="screenshots/secim.jpeg" width="250"/>

---

## 👑 Admin Panel

<img src="screenshots/admin.jpeg" width="250"/>