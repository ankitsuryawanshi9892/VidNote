import youtube_dl
import os

def download_video(url, output_path='output/video.mp4'):
    """
    Download a YouTube video to the specified path.
    Returns the path to the downloaded video or None if failed.
    """
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'mp4',
        'quiet': True  # Suppress console output
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if os.path.exists(output_path):
            return output_path
        return None
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None
    