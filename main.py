import nltk
import os
from youtube_downloader import download_video, get_video_duration
from slide_detector import detect_slides
from audio_processor import extract_and_transcribe_audio
from content_processor import process_content
from text_file_generator import create_text_file

def initialize_nltk():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK punkt tokenizer...")
        nltk.download('punkt')

def get_dynamic_slide_params(duration):
    """
    Determine slide detection parameters based on video duration (in seconds).
    """
    if duration <= 300:  # Short video: <= 5 minutes
        return {
            'threshold': 15,
            'min_duration': 2,
            'fps': 5
        }
    elif 300 < duration <= 900:  # Medium video: 5-15 minutes
        return {
            'threshold': 25,
            'min_duration': 4,
            'fps': 5
        }
    else:  # Long video: > 15 minutes
        return {
            'threshold': 35,
            'min_duration': 6,
            'fps': 2
        }

def main():
    initialize_nltk()
    
    url = input("Enter YouTube video URL: ").strip()
    
    print("\nFetching video duration...")
    duration = get_video_duration(url)
    if duration == 0:
        print("Could not determine video duration. Using default parameters.")
    
    print(f"Video duration: {duration:.2f} seconds")
    
    slide_params = get_dynamic_slide_params(duration)
    print(f"Using slide detection parameters: {slide_params}")
    
    print("\nDownloading video...")
    video_path = download_video(url)
    if not video_path:
        print("Video download failed.")
        return

    print("\nDetecting slides...")
    slide_texts = detect_slides(video_path, **slide_params)
    
    print("\nProcessing audio...")
    audio_text = extract_and_transcribe_audio(video_path)
    print("Audio Text:", audio_text)
    
    print("\nProcessing content...")
    combined_content = slide_texts + ([audio_text] if audio_text else [])
    processed_content = process_content(combined_content)
    
    print("\nGenerating concise notes...")
    output_file = create_text_file(processed_content)
    
    if output_file:
        print(f"\nSUCCESS! Notes generated at: {output_file}")
        with open(output_file, 'r') as f:
            print("\nNOTES PREVIEW:")
            print(f.read())
        
        try:
            os.remove(video_path)
            print(f"\nVideo file deleted: {video_path}")
        except Exception as e:
            print(f"\nError deleting video file: {e}")
    else:
        print("Failed to create notes file")

if __name__ == "__main__":
    main()
