from datetime import datetime
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# توکن ربات شما از BotFather
BOT_TOKEN = "8664091459:AAG4p3wirjtVcRbz1439dDZc4KZMsoL1_uw"

# لینک مینی‌اپ Netlify
MINI_APP_URL = "https://heroic-licorice-7fd7d8.netlify.app/"

def get_countdown_text():
    """محاسبه زمان باقی‌مانده تا ۱۰ سپتامبر (۲۰ شهریور)"""
    tehran_tz = pytz.timezone("Asia/Tehran")
    now = datetime.now(tehran_tz)
    
    target_year = now.year
    birth_date = tehran_tz.localize(datetime(target_year, 9, 10, 0, 0, 0))
    
    # اگر تاریخ امسال گذشته باشد، برای سال بعد محاسبه می‌کند
    if now > birth_date:
        birth_date = tehran_tz.localize(datetime(target_year + 1, 9, 10, 0, 0, 0))
        
    diff = birth_date - now
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    if days == 0 and hours == 0 and minutes == 0:
        return "🎉 امروز روز تولد حدیثه‌ست! تولدت مبارک! 🥳🎈"
    
    return (
        f"⏳ **چقدر مونده تا تولد حدیثه؟** 🍃\n\n"
        f"📅 **{days}** روز\n"
        f"⏰ **{hours}** ساعت\n"
        f"⏱️ **{minutes}** دقیقه\n\n"
        f"🌸 چشم‌انتظار طلوع ۲۰ شهریور..."
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پیام خوش‌آمدگویی و کیبورد شیشه ای"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="ورود به جهان سبز حدیثه 🍃🐤", 
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ],
        [
            InlineKeyboardButton(
                text="⏳ روزشمار تولد ۲۰ شهریور", 
                callback_data="countdown"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "سلام! 👋✨\n\n"
        "به ربات اختصاصی تولد حدیثه خوش آمدید 🌿\n"
        "یکی از گزینه‌های زیر رو انتخاب کنید 👇"
    )

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت دکمه روزشمار"""
    query = update.callback_query
    await query.answer()

    if query.data == "countdown":
        countdown_msg = get_countdown_text()
        
        keyboard = [
            [
                InlineKeyboardButton(
                    text="ورود به مینی‌اپ 🍃🐤", 
                    web_app=WebAppInfo(url=MINI_APP_URL)
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(countdown_msg, reply_markup=reply_markup, parse_mode="Markdown")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    
    print("ربات با موفقیت فعال شد...")
    app.run_polling()