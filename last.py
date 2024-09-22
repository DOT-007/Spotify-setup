import telebot
import yt_dlp
import os


API_TOKEN ='7076425481:AAHvROfybxE_vouKr3w1nlzGMAH144ziQ0E'
bot = telebot.TeleBot(API_TOKEN)

user_data = {}

def download_song(url, username, password, output_path='downloads'):
    ydl_opts = {
        'username': username,
        'password': password,
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send /download to start the download process.")

@bot.message_handler(commands=['download'])
def ask_for_url(message):
    msg = bot.reply_to(message, "Please enter the YouTube URL:")
    bot.register_next_step_handler(msg, process_url_step)

def process_url_step(message):
    try:
        chat_id = message.chat.id
        url = message.text
        user_data[chat_id] = {'url': url}
        msg = bot.reply_to(message, "Please enter your username:")
        bot.register_next_step_handler(msg, process_username_step)
    except Exception as e:
        bot.reply_to(message, 'Oops! Something went wrong.')

def process_username_step(message):
    try:
        chat_id = message.chat.id
        username = message.text
        user_data[chat_id]['username'] = username
        msg = bot.reply_to(message, "Please enter your password:")
        bot.register_next_step_handler(msg, process_password_step)
    except Exception as e:
        bot.reply_to(message, 'Oops! Something went wrong.')

def process_password_step(message):
    try:
        chat_id = message.chat.id
        password = message.text
        user_data[chat_id]['password'] = password
        bot.reply_to(message, "Downloading the song, please wait...")
        url = user_data[chat_id]['url']
        username = user_data[chat_id]['username']
        password = user_data[chat_id]['password']
        download_song(url, username, password)
        bot.reply_to(message, "Download complete! Sending the file...")
        for file in os.listdir('downloads'):
            if file.endswith('.mp3'):
                with open(f'downloads/{file}', 'rb') as audio:
                    bot.send_audio(chat_id, audio)
                os.remove(f'downloads/{file}')
    except Exception as e:
        bot.reply_to(message, 'Oops! Something went wrong.')

bot.polling()
