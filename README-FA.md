### Telegram Phone Lookup Bot - ربات تلگرام جستجو هویت شماره تلفن

| 🇺🇸 [English](README.md) | 🇮🇷 [Persian](README-FA.md) |
|--------------------------|----------------------------|
<br>

## توضیحات (فارسی)

### معرفی پروژه

ربات تلگرامی Telegram Phone Lookup Bot به شما امکان می‌دهد تا اطلاعات مرتبط با شماره‌های تلفن را از سرویس‌های مختلف مثل TrueCaller، Numberbook، Numverify، OpenCNAM و دیتابیس محلی بررسی کنید. این ربات همچنین امکانات مدیریتی برای مدیران فراهم می‌کند تا آمار و گزارشات مربوط به کاربران و جستجوهای انجام‌شده را مشاهده و مدیریت کنند.

### امکانات

- **بررسی شماره تلفن**: بررسی شماره تلفن از سرویس‌های TrueCaller، Numberbook، Numverify، OpenCNAM و دیتابیس محلی.
- **مدیریت کاربران**: امکان محدود کردن و رفع محدودیت کاربران.
- **افزودن مدیران**: افزودن و مشاهده لیست مدیران.
- **افزودن کاربران مجاز**: افزودن و مشاهده لیست کاربران مجاز.
- **آمار و گزارشات**: مشاهده گزارشات و آمار جستجوهای انجام‌شده توسط کاربران.

### نصب و راه‌اندازی

1. **کلون کردن ریپازیتوری**

   ```sh
   git clone https://github.com/clonerdev/Telegram-Phone-Lookup-Bot.git
   cd Telegram-Phone-Lookup-Bot
   ```

2. **ایجاد و فعال‌سازی محیط مجازی**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **نصب وابستگی‌ها**

   ```sh
   pip install -r requirements.txt
   ```

4. **تنظیم متغیرهای محیطی**

   فایل `.env` را در دایرکتوری اصلی پروژه ایجاد کرده و متغیرهای زیر را تنظیم کنید:

   ```env
   TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
   TRUECALLER_API_KEY=YOUR_TRUECALLER_API_KEY
   NUMBERBOOK_API_KEY=YOUR_NUMBERBOOK_API_KEY
   NUMVERIFY_API_KEY=YOUR_NUMVERIFY_API_KEY
   OPENCNAM_API_KEY=YOUR_OPENCNAM_API_KEY
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   ADMIN_USER_ID=YOUR_TELEGRAM_USER_ID
   ```

5. **راه‌اندازی پایگاه داده**

   ```sh
   python -c "from database import init_db; init_db()"
   ```

6. **اجرای ربات**

   ```sh
   python bot.py
   ```

### پیشنهادات برای نسخه‌های آینده

- **افزودن سرویس‌های جدید**: اضافه کردن سرویس‌های جدید برای بررسی شماره‌ها.
- **پشتیبانی از زبان‌های دیگر**: اضافه کردن پشتیبانی از زبان‌های دیگر به ربات.
- **بهبود رابط کاربری**: اضافه کردن امکانات جدید به رابط کاربری و بهبود ظاهر آن.
- **ایجاد سیستم امتیازدهی**: اضافه کردن سیستم امتیازدهی برای کاربران جهت محدود کردن تعداد جستجوها.
