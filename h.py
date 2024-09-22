import telebot
import subprocess
import os

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('7321371301:AAFi-u2DhdnZgHy0i2pA2aUwyXcJFuehmuY')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me a Spotify link to download.")

@bot.message_handler(func=lambda message: True)
def download_song(message):
    url = message.text
    bot.reply_to(message, "Downloading your song...")
    try:
        # Download the song using spotdl
        subprocess.run(['spotdl', url])
        
        # Find the downloaded file (assuming it's in the current directory)
        for file in os.listdir('.'):
            if file.endswith('.mp3'):
                with open(file, 'rb') as audio:
                    bot.send_audio(message.chat.id, audio)
                os.remove(file)  # Remove the file after sending
                break
        bot.reply_to(message, "Download complete!")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

bot.polling()




