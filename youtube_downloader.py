import yt_dlp as youtube_dl
import os

def download_video(url, output_path='output/video.mp4'):
    """
    Download a YouTube video to the specified path using yt-dlp.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'mp4',
        'quiet': True
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_path if os.path.exists(output_path) else None
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None
