import logging
from telegram import Update, ParseMode, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import re
import os

from config import TELEGRAM_BOT_TOKEN, ADMIN_USER_ID
from database import init_db, save_search, save_user, restrict_user, unrestrict_user
from services import check_truecaller, check_numberbook, check_numverify, check_opencnam, check_local_database

# تنظیمات مربوط به لاگ‌ها
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# تابع برای بررسی شماره‌های ایران
def is_iranian_number(number):
    return re.match(r'^\+989\d{9}$', number) or re.match(r'^09\d{9}$', number)

# تابع برای بررسی شماره‌های بین‌المللی
def is_valid_number(number):
    return re.match(r'^\+?\d{10,15}$', number)

# تابع برای پاسخ به دستور استعلام شماره
def check_number(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user.username
    user_id = update.message.from_user.id
    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute('SELECT phone_number, restricted FROM users WHERE user=? AND user_id=?', (user, user_id))
    result = c.fetchone()
    conn.close()

    if not result:
        update.message.reply_text('لطفاً ابتدا شماره تلفن تلگرام خود را با ربات به اشتراک بگذارید.')
        request_contact_button = KeyboardButton('اشتراک‌گذاری شماره تلفن', request_contact=True)
        update.message.reply_text('برای استفاده از ربات، باید شماره تلفن خود را به اشتراک بگذارید.', 
                                  reply_markup=ReplyKeyboardMarkup([[request_contact_button]], one_time_keyboard=True))
        return

    phone_number, restricted = result
    if restricted:
        update.message.reply_text('شما مجاز به استفاده از این ربات نیستید.')
        return

    if not is_iranian_number(phone_number):
        update.message.reply_text('فقط کاربران با شماره‌های ایرانی مجاز به استفاده از این ربات هستند.')
        return

    if len(context.args) != 1:
        update.message.reply_text('لطفاً شماره مورد نظر را وارد کنید.')
        return

    number = context.args[0]
    if not is_valid_number(number):
        update.message.reply_text('لطفاً یک شماره معتبر وارد کنید.')
        return

    response = f"شماره: {number}\n\n"
    response += "_________________\nTrueCaller:\n"
    truecaller_result = check_truecaller(number)
    response += str(truecaller_result) if truecaller_result else "نتیجه‌ای یافت نشد.\n"
    response += "_________________\nNumberbook:\n"
    numberbook_result = check_numberbook(number)
    response += str(numberbook_result) if numberbook_result else "نتیجه‌ای یافت نشد.\n"
    response += "_________________\nNumverify:\n"
    numverify_result = check_numverify(number)
    response += str(numverify_result) if numverify_result else "نتیجه‌ای یافت نشد.\n"
    response += "_________________\nOpenCNAM:\n"
    opencnam_result = check_opencnam(number)
    response += str(opencnam_result) if opencnam_result else "نتیجه‌ای یافت نشد.\n"
    response += "_________________\nLocal Database:\n"
    local_result = check_local_database(number)
    response += str(local_result) if local_result else "نتیجه‌ای یافت نشد.\n"

    context.bot.send_message(chat_id=user_id, text=response, parse_mode=ParseMode.MARKDOWN)
    save_search(user, user_id, number, response)

# تابع برای دریافت و ذخیره شماره تلفن کاربران
def contact_handler(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user.username
    user_id = update.message.from_user.id
    phone_number = update.message.contact.phone_number

    save_user(user, user_id, phone_number)
    update.message.reply_text('شماره تلفن شما ذخیره شد. اکنون می‌توانید از ربات استفاده کنید.')

# تابع برای مشاهده آمار و گزارشات
def view_stats(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if str(user_id) != ADMIN_USER_ID:
        update.message.reply_text('شما مجاز به استفاده از این دستور نیستید.')
        return

    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute('SELECT user, user_id, number, timestamp FROM history')
    rows = c.fetchall()
    conn.close()

    response = 'آمار و گزارشات:\n\n'
    for row in rows:
        response += f"User: {row[0]}, ID: {row[1]}, Number: {row[2]}, Timestamp: {row[3]}\n"

    update.message.reply_text(response)

# تابع برای محدود کردن کاربران
def restrict_user_command(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if str(user_id) != ADMIN_USER_ID:
        update.message.reply_text('شما مجاز به استفاده از این دستور نیستید.')
        return

    if len(context.args) != 2:
        update.message.reply_text('لطفاً نام کاربری و شناسه کاربر را وارد کنید.')
        return

    user = context.args[0]
    user_id = int(context.args[1])

    restrict_user(user, user_id)
    update.message.reply_text(f'کاربر {user} با شناسه {user_id} محدود شد.')

# تابع برای رفع محدودیت کاربران
def unrestrict_user_command(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if str(user_id) != ADMIN_USER_ID:
        update.message.reply_text('شما مجاز به استفاده از این دستور نیستید.')
        return

    if len(context.args) != 2:
        update.message.reply_text('لطفاً نام کاربری و شناسه کاربر را وارد کنید.')
        return

    user = context.args[0]
    user_id = int(context.args[1])

    unrestrict_user(user, user_id)
    update.message.reply_text(f'محدودیت کاربر {user} با شناسه {user_id} رفع شد.')

# تابع برای افزودن مدیران
def add_admin(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if str(user_id) != ADMIN_USER_ID:
        update.message.reply_text('شما مجاز به استفاده از این دستور نیستید.')
        return

    if len(context.args) != 2:
        update.message.reply_text('لطفاً نام کاربری و شناسه کاربر را وارد کنید.')
        return

    user = context.args[0]
    user_id = int(context.args[1])

    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO admins (user, user_id) VALUES (?, ?)', (user, user_id))
    conn.commit()
    conn.close()

    update.message.reply_text(f'کاربر {user} با شناسه {user_id} به عنوان مدیر اضافه شد.')

# تابع برای مشاهده لیست مدیران
def view_admins(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if str(user_id) != ADMIN_USER_ID:
        update.message.reply_text('شما مجاز به استفاده از این دستور نیستید.')
        return

    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute('SELECT user, user_id FROM admins')
    rows = c.fetchall()
    conn.close()

    response = 'لیست مدیران:\n\n'
    for row in rows:
        response += f"User: {row[0]}, ID: {row[1]}\n"

    update.message.reply_text(response)

# تابع برای افزودن کاربران مجاز
def add_authorized_user(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if str(user_id) != ADMIN_USER_ID:
        update.message.reply_text('شما مجاز به استفاده از این دستور نیستید.')
        return

    if len(context.args) != 2:
        update.message.reply_text('لطفاً نام کاربری و شماره تلفن کاربر را وارد کنید.')
        return

    user = context.args[0]
    phone_number = context.args[1]

    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO authorized_users (user, phone_number) VALUES (?, ?)', (user, phone_number))
    conn.commit()
    conn.close()

    update.message.reply_text(f'کاربر {user} با شماره تلفن {phone_number} به لیست کاربران مجاز اضافه شد.')

# تابع برای مشاهده لیست کاربران مجاز
def view_authorized_users(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if str(user_id) != ADMIN_USER_ID:
        update.message.reply_text('شما مجاز به استفاده از این دستور نیستید.')
        return

    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute('SELECT user, phone_number FROM authorized_users')
    rows = c.fetchall()
    conn.close()

    response = 'لیست کاربران مجاز:\n\n'
    for row in rows:
        response += f"User: {row[0]}, Phone Number: {row[1]}\n"

    update.message.reply_text(response)

def main():
    # توکن ربات تلگرام
    TOKEN = TELEGRAM_BOT_TOKEN

    # تنظیم پایگاه داده
    init_db()

    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("check", check_number))
    dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))
    dispatcher.add_handler(CommandHandler("stats", view_stats))
    dispatcher.add_handler(CommandHandler("restrict", restrict_user_command))
    dispatcher.add_handler(CommandHandler("unrestrict", unrestrict_user_command))
    dispatcher.add_handler(CommandHandler("addadmin", add_admin))
    dispatcher.add_handler(CommandHandler("viewadmins", view_admins))
    dispatcher.add_handler(CommandHandler("adduser", add_authorized_user))
    dispatcher.add_handler(CommandHandler("viewusers", view_authorized_users))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
