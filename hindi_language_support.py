from speech_recognition import Recognizer, AudioData
import requests
import json

class HindiRecognizer:
    @staticmethod
    def recognize(audio_data: AudioData):
        """Custom recognizer for Hindi language"""
        try:
            # Use Google's speech recognition with Hindi language
            recognizer = Recognizer()
            text = recognizer.recognize_google(audio_data, language="hi-IN")
            return text
        except Exception as e:
            print(f"Hindi recognition error: {e}")
            return None
            