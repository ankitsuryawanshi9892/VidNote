# from slide_detector import detect_slides

# slides = detect_slides('English reading practice #english #englishpractice.mp4')
# # for slide in slides:
# #     print(slide)
# print(f"Detected {len(slides)} slides")

from slide_detector import detect_slides

slide_texts = detect_slides('English reading practice #english #englishpractice.mp4')

for i, text in enumerate(slide_texts, 1):
    print(f"--- Slide {i} ---")
    print(text)
    print("\n")

print(f"Detected {len(slide_texts)} slides with text.")
