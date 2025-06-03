import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os

def extract_and_transcribe_audio(video_path):
    """Robust audio processing with proper imports"""
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        temp_audio = os.path.join(temp_dir, "audio.wav")
        
        # Convert video to audio using AudioSegment
        audio = AudioSegment.from_file(video_path)
        audio.export(temp_audio, format="wav")
        
        # Initialize recognizer
        r = sr.Recognizer()
        
        with sr.AudioFile(temp_audio) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language='en-IN')
        
        # Clean up
        os.remove(temp_audio)
        os.rmdir(temp_dir)
        return text
        
    except Exception as e:
        print(f"Audio processing error: {e}")
        if 'temp_audio' in locals() and os.path.exists(temp_audio):
            os.remove(temp_audio)
        if 'temp_dir' in locals() and os.path.exists(temp_dir):
            os.rmdir(temp_dir)
        return None
    