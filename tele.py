import telebot
import yt_dlp as youtube_dl

# Initialize your Telegram bot with your bot token
bot_token = "7076425481:AAHvROfybxE_vouKr3w1nlzGMAH144ziQ0E"
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me a YouTube URL, and I'll download the song for you.")

@bot.message_handler(func=lambda message: True)
def download_song(message):
    try:
        url = message.text
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',  # Output file name template
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'Unknown')
            bot.reply_to(message, f"Downloading: {title}...")

            # Download the song
            ydl.download([url])
            bot.reply_to(message, f"Downloaded: {title}. Enjoy!")

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

if __name__ == "__main__":
    bot.polling()
