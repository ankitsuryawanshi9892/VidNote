from slide_detector import detect_slides
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_pdf(text_list, output_file='output/notes.pdf'):
    """
    Create a PDF from a list of extracted texts.
    """
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        c = canvas.Canvas(output_file, pagesize=letter)
        c.setFont("Helvetica", 12)
        y = 750  # Starting y-coordinate

        for slide_num, text in enumerate(text_list, 1):
            c.drawString(50, y, f"Slide {slide_num}:")
            y -= 20
            for line in text.split('\n'):
                if y < 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = 750
                c.drawString(50, y, line[:100])  # Truncate long lines
                y -= 20
            y -= 20  # Space between slides
        c.save()
        print(f"PDF created: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return None

def main():
    # Step 1: Detect slides and extract texts
    slide_texts = detect_slides('English reading practice #english #englishpractice.mp4')

    for i, text in enumerate(slide_texts, 1):
        print(f"--- Slide {i} ---")
        print(text)
        print("\n") 

    print(f"Detected {len(slide_texts)} slides with text.")

    # Step 2: Create PDF from extracted texts
    create_pdf(slide_texts, output_file='output/notes.pdf')

if __name__ == "__main__":
    main()
