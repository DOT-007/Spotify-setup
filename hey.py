import telebot
import subprocess
import os

API_TOKEN = '7076425481:AAFDW1z2Gn8jo2DD6BKLTGaHqaylbHgRWvA'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    src = message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    # Convert .mkv to .m3u8
    dest = src.rsplit('.', 1)[0] + '.m3u8'
    command = f"ffmpeg -i {src} -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls {dest}"
    subprocess.run(command, shell=True)
    
    # Send the converted file
    with open(dest, 'rb') as converted_file:
        bot.send_document(message.chat.id, converted_file)
    
    # Clean up files
    os.remove(src)
    os.remove(dest)

bot.polling()
