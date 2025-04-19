import telebot
import requests
import base64
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# توكن البوت
bot = telebot.TeleBot("8023861006:AAHGAZZs540qVAJVAsR1kNnluIj7nTwzW5U")

# مفتاح API الخاص بـ imgbb
IMGBB_API_KEY = "9e4bd84dfb5a38bae1caabf4d1b14587"

# استقبال الصور ورفعها
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.send_message(message.chat.id, "جارٍ رفع الصورة...")

    # الحصول على الملف من تيليجرام
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # تحويل الصورة إلى base64
    encoded_image = base64.b64encode(downloaded_file).decode("utf-8")

    # رفع الصورة إلى imgbb
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": IMGBB_API_KEY,
        "image": encoded_image
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        image_url = response.json()["data"]["url"]

        # إنشاء زر لنسخ الرابط
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("نسخ الرابط", url=image_url))

        bot.send_message(message.chat.id, f"تم رفع الصورة بنجاح:\n{image_url}", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "حدث خطأ أثناء رفع الصورة. حاول مجددًا.")

# التعامل مع الرسائل غير الصور
@bot.message_handler(func=lambda message: True)
def handle_other(message):
	bot.send_message(message.chat.id, "هذا البوت مخصص لرفع الصور.\nمن فضلك أرسل صورة وسأعطيك رابط مباشر لها.\nتمت برمجة هذا البوت من قِبل ثابت الذُعمري.")

# تشغيل البوت
print("✅ البوت يعمل الآن... أرسل صورة")
bot.infinity_polling()
