import cv2
import easyocr
import numpy as np

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(frame):
    """
    Preprocess frame for better OCR accuracy.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Enhance contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    # Light denoising to preserve small text
    denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
    return denoised

# Load the image
frame = cv2.imread('Screenshot (203).png')
if frame is None:
    print("Error: Could not load Screenshot (203).png")
else:
    # Crop the image to exclude YouTube UI (top bar, bottom progress bar)
    h, w = frame.shape[:2]
    cropped = frame[50:h-50, 0:w]  # Adjust cropping as needed

    # Preprocess the cropped image
    processed_frame = preprocess_image(cropped)

    # Save the preprocessed image for inspection
    cv2.imwrite('preprocessed_image.png', processed_frame)

    # Extract text using EasyOCR
    try:
        results = reader.readtext(processed_frame, detail=0, paragraph=True,
                                 contrast_ths=0.3, mag_ratio=1.5)
        text = ' '.join(results)
        # Post-process to clean up
        text = text.replace(':', ' ').replace('°', '').replace('©', '').replace('=', '')
        text = ' '.join(text.split())  # Normalize spaces
        print("Extracted text:")
        print(text if text.strip() else "No text detected")
    except Exception as e:
        print(f"Error in OCR: {e}")
        print("OCR failed")
        