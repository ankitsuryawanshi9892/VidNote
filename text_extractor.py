import cv2
import pytesseract
from PIL import Image
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(frame):
    """
    Preprocess frame for better OCR accuracy.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kernel = np.array([[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]])
    sharpened = cv2.filter2D(gray, -1, kernel)
    thresh = cv2.adaptiveThreshold(sharpened, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY, 15, 10)
    denoised = cv2.fastNlMeansDenoising(thresh, None, 30, 7, 21)
    return Image.fromarray(denoised)

def extract_text(frame):
    """
    Extract text from a single frame using Tesseract OCR.
    """
    try:
        pil_image = preprocess_image(frame)
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(pil_image, config=custom_config)
        return text.strip() if text.strip() else "No text detected"
    except Exception as e:
        print(f"Error in OCR: {e}")
        return "OCR failed"


# import cv2
# import easyocr
# import numpy as np

# # Initialize EasyOCR reader (load model once for efficiency)
# reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if you have a compatible GPU

# def preprocess_image(frame):
#     """
#     Preprocess frame for better OCR accuracy.
#     """
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     kernel = np.array([[0, -1, 0],
#                     [-1, 5, -1],
#                     [0, -1, 0]])
#     sharpened = cv2.filter2D(gray, -1, kernel)
#     thresh = cv2.adaptiveThreshold(sharpened, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
#                                 cv2.THRESH_BINARY, 15, 10)
#     denoised = cv2.fastNlMeansDenoising(thresh, None, 30, 7, 21)
#     return denoised

# def extract_text(frame):
#     """
#     Extract text from a single frame using EasyOCR.
#     """
#     try:
#         processed_frame = preprocess_image(frame)
#         # EasyOCR expects a numpy array or image path
#         results = reader.readtext(processed_frame, detail=0, paragraph=True)
#         text = ' '.join(results)  # Combine all detected text
#         return text.strip() if text.strip() else "No text detected"
#     except Exception as e:
#         print(f"Error in OCR: {e}")
#         return "OCR failed"
    