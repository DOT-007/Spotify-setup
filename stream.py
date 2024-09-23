import os
import telebot
import subprocess

BOT_TOKEN = '7076425481:AAFxNuWGFc0VqZDSQT0ON5-xX1cjtaavYmo'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me a movie file to convert to M3U8.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'movie.mp4'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Convert the movie file to M3U8
    dest = 'output.m3u8'
    command = f"ffmpeg -i {src} -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls {dest}"
    subprocess.run(command, shell=True)

    # Send the converted file
    with open(dest, 'rb') as video:
        bot.send_document(message.chat.id, video)

bot.polling()
