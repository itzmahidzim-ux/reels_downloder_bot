import telebot
import os
from yt_dlp import YoutubeDL
from telebot import types

# --- ⚙️ কনফিগারেশন ---
# আপনার নতুন টোকেনটি এখানে বসানো হয়েছে
API_TOKEN = '8063826212:AAFaZmvcrI2Et2UPn1fIZeXk0iQtKRKLfTQ'
bot = telebot.TeleBot(API_TOKEN)

# ফাইল রাখার জন্য ফোল্ডার তৈরি
if not os.path.exists('social_reels'):
    os.makedirs('social_reels')

# --- ⌨️ কিবোর্ড বাটন (নিচে স্থায়ী চাবির মতো) ---
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("📥 Download Now")
    btn2 = types.KeyboardButton("📂 View Video")
    markup.add(btn1, btn2)
    return markup

# --- 🚀 স্টার্ট কমান্ড ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_msg = (
        "🌟 **Social Reels Downloader** 🌟\n\n"
        "আমি ফেসবুক, টিকটক এবং ইনস্টাগ্রাম রিলস ডাউনলোড করতে পারি।\n"
        "নিচের বাটনগুলো ব্যবহার করুন অথবা সরাসরি লিঙ্ক পাঠান।"
    )
    bot.reply_to(message, welcome_msg, reply_markup=main_keyboard(), parse_mode="Markdown")

# --- 💬 মেসেজ ও লিঙ্ক হ্যান্ডলার ---
@bot.message_handler(func=lambda message: True)
def handle_reels(message):
    text = message.text.strip()

    # বাটন ক্লিক হ্যান্ডল
    if text == "📥 Download Now":
        bot.send_message(message.chat.id, "🔗 দয়া করে ফেসবুক, টিকটক বা ইনস্টাগ্রাম রিলস লিঙ্কটি এখানে পাঠান।")
        return
    
    elif text == "📂 View Video":
        bot.send_message(message.chat.id, "🎬 আপনার ডাউনলোড করা ভিডিওগুলো চ্যাটের ঠিক ওপরেই দেখতে পাবেন।")
        return

    # লিঙ্ক চেক করা (FB, TikTok, Instagram)
    valid_sites = ['facebook.com', 'fb.watch', 'tiktok.com', 'instagram.com']
    if any(site in text.lower() for site in valid_sites):
        status_msg = bot.reply_to(message, "⏳ **প্রসেসিং হচ্ছে... একটু অপেক্ষা করুন।**")
        
        try:
            # ডাউনলোড সেটিংস (HD Quality)
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'social_reels/%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                file_path = ydl.prepare_filename(info)
            
            # ভিডিও পাঠানো
            with open(file_path, 'rb') as video:
                bot.send_video(
                    message.chat.id, 
                    video, 
                    caption=f"✅ ডাউনলোড সম্পন্ন!\n📌 প্ল্যাটফর্ম: {info.get('extractor_key', 'Social Media')}",
                    timeout=300
                )

            # ফাইল মুছে ফেলা (মেমোরি বাঁচাতে)
            if os.path.exists(file_path):
                os.remove(file_path)
            bot.delete_message(message.chat.id, status_msg.message_id)

        except Exception as e:
            bot.edit_message_text(f"❌ এরর: ভিডিওটি পাওয়া যায়নি বা লিঙ্কটি প্রাইভেট।", message.chat.id, status_msg.message_id)
    
    else:
        bot.reply_to(message, "⚠️ শুধু ফেসবুক, টিকটক বা ইনস্টাগ্রাম রিলস লিঙ্ক পাঠান।")

# --- ⚡ বট চালু করা ---
print("🚀 Your New Reels Bot is Running...")
bot.polling(none_stop=True)


