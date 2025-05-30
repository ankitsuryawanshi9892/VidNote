import cv2
from text_extractor import extract_text
import difflib

def is_significantly_different(new_text, existing_texts, similarity_threshold=0.8):
    """
    Check if the new_text is significantly different from any existing text
    based on difflib similarity.
    """
    for existing in existing_texts:
        similarity = difflib.SequenceMatcher(None, new_text, existing).ratio()
        if similarity > similarity_threshold:
            # Too similar to an existing slide; skip it.
            return False
    return True

def detect_slides(video_path, threshold=5, min_duration=3, fps=1):
    """
    Detect slide frames and extract text from them, removing duplicates using difflib.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return []

    slide_texts = []
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
                        text = extract_text(frame)
                        if text != "No text detected":
                            if is_significantly_different(text, slide_texts):
                                slide_texts.append(text)
                else:
                    static_frames = 0
            prev_frame = gray
        frame_count += 1

    cap.release()
    return slide_texts
