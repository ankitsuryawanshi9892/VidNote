# import cv2
# import numpy as np

# def detect_slides(video_path, threshold=5, min_duration=3, fps=1):
#     """
#     Detect slide frames in a video.
#     Returns a list of frames (as numpy arrays) representing unique slides.
#     """
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         print("Error: Could not open video.")
#         return []

#     slide_frames = []
#     prev_frame = None
#     frame_count = 0
#     static_frames = 0
#     frame_rate = cap.get(cv2.CAP_PROP_FPS)
#     frame_interval = int(frame_rate / fps)  # Process 1 frame per second

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         if frame_count % frame_interval == 0:
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             if prev_frame is not None:
#                 diff = cv2.absdiff(gray, prev_frame)
#                 mean_diff = cv2.mean(diff)[0]
#                 if mean_diff < threshold:
#                     static_frames += 1
#                     if static_frames >= min_duration * fps:
#                         slide_frames.append(frame)
#                 else:
#                     static_frames = 0
#             prev_frame = gray
#         frame_count += 1

#     cap.release()
#     # Remove duplicates by comparing frames
#     unique_frames = []
#     for frame in slide_frames:
#         if not unique_frames or not np.array_equal(frame, unique_frames[-1]):
#             unique_frames.append(frame)
#     return unique_frames

import cv2
import numpy as np
import pytesseract
from PIL import Image

def detect_slides(video_path, threshold=5, min_duration=3, fps=1):
    """Detect slide frames and extract text from them."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return []

    slide_texts = []  # Store extracted text from slides
    prev_frame = None
    frame_count = 0
    static_frames = 0
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(frame_rate / fps)

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
                    static_frames += 1
                    if static_frames >= min_duration * fps:
                        # Extract text from the slide
                        text = extract_text_from_frame(frame)
                        if text.strip():  # Only add if text is detected
                            slide_texts.append(text)
                else:
                    static_frames = 0
            prev_frame = gray
        frame_count += 1

    cap.release()
    return slide_texts

def extract_text_from_frame(frame):
    """Extract text from a single frame using OCR."""
    # Preprocess image for better OCR results
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Use Tesseract OCR
    text = pytesseract.image_to_string(thresh, lang='eng')
    return text.strip()
