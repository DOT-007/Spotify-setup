import requests
import telebot
import yt_dlp
from moviepy.editor import *

# Initialize the Telegram bot with your API token
TOKEN = '7321371301:AAG-ETsOspoFKdhlFZBDvLyjm28P9tFkMMw'
bot = telebot.TeleBot(TOKEN)

# Define a function to handle the /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! I'm your YouTube-to-MP3 bot. Send me a YouTube link, and I'll convert it to MP3 for you!")

# Define a function to handle text messages (containing YouTube URLs)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        url = message.text
        ydl_opts = {'format': 'bestaudio/best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info['title']
            video_url = info['url']

        # Download the video
        video_path = f"{video_title}.mp4"
        video = VideoFileClip(video_url)
        video.write_videofile(video_path)

        # Convert to MP3
        audio_path = f"{video_title}.mp3"
        video.audio.write_audiofile(audio_path)

        # Send the MP3 back to the user
        bot.send_audio(message.chat.id, open(audio_path, 'rb'))

    except Exception as e:
        bot.reply_to(message, f"Oops! Something went wrong. Please check the URL and try again. Error: {str(e)}")

# Run the bot
bot.polling()
