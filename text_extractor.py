import cv2
import pytesseract
from PIL import Image
import numpy as np

# Set Tesseract path (adjust if different)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(frame):
    """
    Preprocess frame for better OCR accuracy.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(thresh)

def extract_text(frame):
    """
    Extract text from a single frame using Tesseract OCR.
    """
    try:
        pil_image = preprocess_image(frame)
        text = pytesseract.image_to_string(pil_image, config='--psm 6')
        return text.strip() if text.strip() else "No text detected"
    except Exception as e:
        print(f"Error in OCR: {e}")
        return "OCR failed"
    