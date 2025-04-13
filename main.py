import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from PIL import Image
import io
import random

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")
user_languages = {}

def fake_analysis():
    directions = ['شراء', 'بيع']
    durations = ['دقيقة واحدة', 'دقيقتان', '5 دقائق']
    models = ['نموذج الرأس والكتفين', 'نموذج القاع المزدوج', 'نموذج المثلث الصاعد']
    return {
        "الاتجاه": random.choice(directions),
        "المدة": random.choice(durations),
        "النموذج": random.choice(models)
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['العربية', 'English']]
    await update.message.reply_text(
        "مرحبًا بك! اختر لغتك / Please choose your language:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.message.text
    user_languages[update.message.from_user.id] = lang
    await update.message.reply_text(f"تم اختيار اللغة: {lang}" if lang == "العربية" else f"Language set to: {lang}")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    lang = user_languages.get(user_id, "العربية")

    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()
    img = Image.open(io.BytesIO(photo_bytes))

    result = fake_analysis()

    if lang == "العربية":
        response = f"""📊 تحليل الشارت:
📈 الاتجاه: {result['الاتجاه']}
⏱️ مدة الصفقة: {result['المدة']}
📐 النموذج الفني: {result['النموذج']}
🎯 نسبة النجاح المتوقعة: 95%"""
    else:
        response = f"""📊 Chart Analysis:
📈 Direction: {result['الاتجاه']}
⏱️ Trade Duration: {result['المدة']}
📐 Pattern: {result['النموذج']}
🎯 Expected Success Rate: 95%"""

    await update.message.reply_text(response)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_language))
app.add_handler(MessageHandler(filters.PHOTO, handle_image))

print("🤖 البوت شغال الآن...")
app.run_polling()
