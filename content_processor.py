import re
from googletrans import Translator

class ContentProcessor:
    def __init__(self):
        self.translator = Translator()
        self.common_errors = {
            'cEP': 'ASD',
            'SD “AKA': 'also known as',
            'Tey ay see ST': '',
            r'\$': 's',  # Fix dollar sign OCR errors
            r'\b\w\w\b': ''  # Remove 2-letter words (common OCR noise)
        }

    def clean_text(self, text):
        """Enhanced cleaning for short video content"""
        if not text:
            return ""
            
        # Standardize quotes and fix common OCR errors
        text = text.replace('“', '"').replace('”', '"')
        
        # Apply common error fixes
        for error, fix in self.common_errors.items():
            text = re.sub(error, fix, text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,;:!?-]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def process_content(self, content_list):
        """Process content with focus on quality over quantity"""
        cleaned = []
        
        for text in content_list:
            clean_text = self.clean_text(text)
            if clean_text and len(clean_text.split()) >= 3:  # Minimum 3 words
                cleaned.append(clean_text)
        
        # Simple deduplication
        unique = []
        seen = set()
        for text in cleaned:
            key = re.sub(r'[^\w\s]', '', text.lower())
            if key not in seen:
                seen.add(key)
                unique.append(text)
        
        return unique

def process_content(content_list):
    return ContentProcessor().process_content(content_list)
