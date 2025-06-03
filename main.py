from youtube_downloader import download_video
from slide_detector import detect_slides
from audio_processor import extract_and_transcribe_audio
from content_processor import process_content
from text_file_generator import create_text_file
import nltk

def initialize_nltk():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK punkt tokenizer...")
        nltk.download('punkt')

def main():
    initialize_nltk()
    
    url = input("Enter YouTube video URL: ").strip()
    print("\nDownloading video...")
    video_path = download_video(url)
    if not video_path:
        print("Video download failed.")
        return

    # Optimized parameters for short videos
    print("\nDetecting slides (optimized for short videos)...")
    slide_params = {
        'threshold': 10,  # Higher threshold for more sensitivity
        'min_duration': 1,  # Shorter duration for brief slides
        'fps': 2  # Higher frame rate for short videos
    }
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
    else:
        print("Failed to create notes file")

if __name__ == "__main__":
    main()
