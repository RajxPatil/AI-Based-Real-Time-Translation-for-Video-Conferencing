# main.py - Main application
from modules.audio_capture import AudioCapture
from modules.audio_preprocessing import AudioPreprocessing
from modules.language_detection import LanguageDetection
from modules.speech_to_text import SpeechToText
from modules.translation import Translation
from modules.subtitle_renderer import SubtitleRenderer
from modules.realtime_subtitle_system import RealTimeSubtitleSystem

# Initialize and run the system
if __name__ == "__main__":
    system = RealTimeSubtitleSystem()
    system.initialize()
    system.start()
