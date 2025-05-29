import yt_dlp
import os

def download_video(url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"Video downloaded to: {os.path.abspath(filename)}")
            return filename
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

url = "https://www.youtube.com/shorts/FW_lQo5zmuw"
video_path = download_video(url)
