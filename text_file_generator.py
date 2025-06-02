# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# import os

# def create_pdf(text_list, output_file='output/notes.pdf'):
#     """
#     Create a PDF from a list of extracted texts.
#     """
#     try:
#         os.makedirs(os.path.dirname(output_file), exist_ok=True)
#         c = canvas.Canvas(output_file, pagesize=letter)
#         c.setFont("Helvetica", 12)
#         y = 750

#         for slide_num, text in enumerate(text_list, 1):
#             c.drawString(50, y, f"Slide {slide_num}:")
#             y -= 20
#             for line in text.split('\n'):
#                 if y < 50:
#                     c.showPage()
#                     c.setFont("Helvetica", 12)
#                     y = 750
#                 c.drawString(50, y, line[:100])
#                 y -= 20
#             y -= 20
#         c.save()
#         print(f"PDF created: {output_file}")
#         return output_file
#     except Exception as e:
#         print(f"Error creating PDF: {e}")
#         return None

import os

def create_text_file(text_list, output_file='output/notes.txt'):
    """
    Create a text file from a list of extracted texts.
    """
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            for slide_num, text in enumerate(text_list, 1):
                f.write(f"Slide {slide_num}:\n")
                f.write(text.strip())
                f.write("\n\n" + "-"*40 + "\n\n")
        print(f"Text file created: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error creating text file: {e}")
        return None
