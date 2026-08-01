const { Telegraf, Markup } = require('telegraf');

// توکن ربات حدیثه
const BOT_TOKEN = '8664091459:AAG4p3wirjtVcRbz1439dDZc4KZMsoL1_uw';
// لینک مینی‌اپ که روی نتلیفای آپلود کردی
const MINI_APP_URL = 'https://leaf-and-chick-hadise.netlify.app'; 

const bot = new Telegraf(BOT_TOKEN);

// محاسبه زمان باقی‌مانده تا ۲۰ شهریور (۱۰ سپتامبر)
function getDaysUntilBirthday() {
    const now = new Date();
    const currentYear = now.getFullYear();
    let targetDate = new Date(currentYear, 8, 10); // سپتامبر ماه ۹ میلادی (اندیس ۸) است

    if (now > targetDate) {
        targetDate = new Date(currentYear + 1, 8, 10);
    }

    const diffTime = targetDate - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
}

// پاسخی که با زدن /start ارسال می‌شود
bot.start((ctx) => {
    const daysLeft = getDaysUntilBirthday();
    
    const keyboard = Markup.inlineKeyboard([
        [Markup.button.webApp('🌿 ورود به جهان سبز حدیثه 🐣', MINI_APP_URL)],
        [Markup.button.callback(`⏳ ${daysLeft} روز تا تولد حدیثه باقی مانده!`, 'countdown_info')]
    ]);

    ctx.reply(
        'سلام! 🌸 به ربات اختصاصی تولد حدیثه خوش آمدی.\n\n' +
        'از دکمه‌های زیر می‌تونی وارد مینی‌اپ بشی یا روزشمار تولد رو ببینی:',
        keyboard
    );
});

// اکشن کلیک روی دکمه روزشمار
bot.action('countdown_info', (ctx) => {
    const daysLeft = getDaysUntilBirthday();
    ctx.answerCbQuery(`🎉 فقط ${daysLeft} روز دیگه تا ۲۰ شهریور مونده!`, { show_alert: true });
});

// خروجی برای محیط سرورلس
module.exports = bot;