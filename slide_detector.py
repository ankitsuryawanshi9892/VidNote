import cv2
import pytesseract
from difflib import SequenceMatcher
import re

def extract_text(image):
    """Improved text extraction with OCR configuration"""
    custom_config = r'--oem 3 --psm 6 -l eng'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text.strip()

def is_significantly_different(new_text, existing_texts, similarity_threshold=0.7):
    """More lenient similarity check for short videos"""
    if not new_text or len(new_text.split()) < 3:
        return False
    for existing in existing_texts:
        similarity = SequenceMatcher(None, new_text, existing).ratio()
        if similarity > similarity_threshold:
            return False
    return True

def detect_slides(video_path, threshold=10, min_duration=1, fps=2):
    """Optimized for short videos"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return []

    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(1, int(frame_rate / fps))
    slide_texts = []
    prev_frame = None
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if prev_frame is not None:
                diff = cv2.absdiff(gray, prev_frame)
                mean_diff = cv2.mean(diff)[0]
                
                if mean_diff < threshold:
                    text = extract_text(frame)
                    if text and is_significantly_different(text, slide_texts):
                        slide_texts.append(text)
            prev_frame = gray
        
        frame_count += 1

    cap.release()
    return slide_texts
