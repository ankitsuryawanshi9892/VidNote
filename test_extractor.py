import cv2
from text_extractor import extract_text

frame = cv2.imread('test_slide.png')  # Or use a frame from slide_detector
text = extract_text(frame)
print(text)

