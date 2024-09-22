import yt_dlp

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

if __name__ == "__main__":
    url = input("Enter the URL of the song: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    download_song(url, username, password)
