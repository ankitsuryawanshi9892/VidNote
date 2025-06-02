from youtube_downloader import download_video
from slide_detector import detect_slides
from pdf_generator import create_text_file

def main():
    # Step 1: Download video
    url = input("Enter YouTube video URL: ").strip()
    video_path = download_video(url)
    if not video_path:
        print("Video download failed.")
        return

    # Step 2: Detect slides and extract text
    slide_texts = detect_slides(video_path)
    if not slide_texts:
        print("No slides or text detected.")
        return

    # Step 3: Create Text File
    pdf_file = create_text_file(slide_texts)
    if pdf_file:
        print(f"All done! PDF generated at: {pdf_file}")
    else:
        print("Failed to create PDF.")

if __name__ == "__main__":
    main()
