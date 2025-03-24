# modules/realtime_subtitle_system.py
import os
import asyncio
import threading
from typing import Dict, Optional
import azure.cognitiveservices.speech as speechsdk # type: ignore

from .audio_capture import AudioCapture
from .audio_preprocessing import AudioPreprocessing
from .language_detection import LanguageDetection
from .speech_to_text import SpeechToText
from .translation import Translation
from .subtitle_renderer import SubtitleRenderer

class RealTimeSubtitleSystem:
    def __init__(self, config=None):
        """Initialize the real-time subtitle system."""
        self.config = config or {}
        
        # Load configuration from environment variables if not provided
        self.azure_config = {
            'speech_key': self.config.get('speech_key', os.environ.get('AZURE_SPEECH_KEY')),
            'speech_region': self.config.get('speech_region', os.environ.get('AZURE_SPEECH_REGION')),
            'translator_key': self.config.get('translator_key', os.environ.get('AZURE_TRANSLATOR_KEY')),
            'translator_region': self.config.get('translator_region', os.environ.get('AZURE_TRANSLATOR_REGION')),
            'language_key': self.config.get('language_key', os.environ.get('AZURE_LANGUAGE_KEY')),
            'language_endpoint': self.config.get('language_endpoint', os.environ.get('AZURE_LANGUAGE_ENDPOINT'))
        }
        
        self.default_language = self.config.get('default_language', 'en')
        self.target_language = self.config.get('target_language', 'en')
        
        # Initialize module instances
        self.audio_capture = None
        self.audio_preprocessing = None
        self.language_detection = None
        self.speech_to_text = None
        self.translation = None
        self.subtitle_renderer = None
        
        # State variables
        self.current_language = self.default_language
        self.is_running = False
        
        # Async event loop
        self.loop = asyncio.new_event_loop()
        
        # GUI thread for subtitle rendering
        self.gui_thread = None
    
    def initialize(self):
        """Initialize all modules."""
        print("Initializing Real-Time Subtitle System...")
        
        # Initialize audio capture
        self.audio_capture = AudioCapture()
        
        # Initialize audio preprocessing
        self.audio_preprocessing = AudioPreprocessing()
        
        # Initialize language detection
        self.language_detection = LanguageDetection({
            'api_key': self.azure_config['language_key'],
            'endpoint': self.azure_config['language_endpoint']
        })
        
        # Initialize speech-to-text
        self.speech_to_text = SpeechToText({
            'api_key': self.azure_config['speech_key'],
            'region': self.azure_config['speech_region'],
            'default_language': self.default_language
        })
        
        # Initialize translation
        self.translation = Translation({
            'api_key': self.azure_config['translator_key'],
            'location': self.azure_config['translator_region'],
            'target_language': self.target_language
        })
        
        # Initialize subtitle renderer in a separate thread for GUI
        self.gui_thread = threading.Thread(target=self._init_subtitle_renderer)
        self.gui_thread.daemon = True
        self.gui_thread.start()
        
        # Set up audio callback
        self.audio_capture.set_audio_callback(self._handle_audio)
        
        # Set up transcription callback
        self.speech_to_text.set_transcription_callback(self._handle_transcription)
        
        print("Initialization complete.")
        return True
    
    def _init_subtitle_renderer(self):
        """Initialize subtitle renderer in a GUI thread."""
        import tkinter as tk
        
        root = tk.Tk()
        root.title("Subtitle Overlay")
        root.geometry("800x200+100+100")
        root.attributes("-topmost", True)
        root.configure(bg='black')
        
        self.subtitle_renderer = SubtitleRenderer({
            'fade_timeout': 5.0,
            'max_lines': 2,
            'font_size': 18
        })
        self.subtitle_renderer.initialize(parent_window=root)
        
        root.mainloop()
    
    def start(self):
        """Start the system."""
        if self.is_running:
            print("System is already running")
            return False
        
        print("Starting Real-Time Subtitle System...")
        
        # Initialize microphone
        mic_initialized = self.audio_capture.initialize_microphone_capture()
        if not mic_initialized:
            print("Failed to initialize microphone")
            return False
        
        # Start audio capture
        self.audio_capture.start_recording()
        
        # Start speech recognition
        self.speech_to_text.start_recognition()
        
        self.is_running = True
        print("System started successfully")
        return True
    
    def stop(self):
        """Stop the system."""
        if not self.is_running:
            print("System is not running")
            return False
        
        print("Stopping Real-Time Subtitle System...")
        
        # Stop audio capture
        self.audio_capture.stop_recording()
        
        # Stop speech recognition
        self.speech_to_text.stop_recognition()
        
        # Clear subtitles
        if self.subtitle_renderer:
            self.subtitle_renderer.clear()
        
        self.is_running = False
        print("System stopped")
        return True
    
    def _handle_audio(self, audio_data):
        """Handle incoming audio data."""
        if not self.is_running:
            return
        
        # Process audio with noise suppression
        processed_audio = self.audio_preprocessing.process_audio(audio_data)
        
        # For Azure Speech SDK, we don't need to manually feed the audio
        # as it's handled by the recognizer's audio config
        # This would be used if we were implementing our own audio feeding mechanism
    
    async def _handle_transcription(self, transcription_result):
        """Handle transcription results."""
        if not self.is_running or not transcription_result.get('text'):
            return
        
        text = transcription_result['text']
        is_final = transcription_result.get('is_final', False)
        
        # Detect language if needed (for longer texts)
        if is_final and len(text) > 15:
            detected_language = await self.language_detection.detect_language(text)
            
            if detected_language and detected_language['language_code'] != self.current_language:
                self.current_language = detected_language['language_code']
                self.speech_to_text.set_language(self.current_language)
                print(f"Detected language changed to: {self.current_language}")
        
        # Translate text if needed
        translation_result = await self.translation.translate_text(text, self.current_language)
        
        # Show subtitle
        if self.subtitle_renderer:
            self.subtitle_renderer.show_subtitle(translation_result['translated_text'])
    
    def set_target_language(self, language_code):
        """Set the target language for translation."""
        if self.translation:
            self.translation.set_target_language(language_code)
    
    def cleanup(self):
        """Clean up all resources."""
        print("Cleaning up resources...")
        
        if self.is_running:
            self.stop()
        
        if self.audio_capture:
            self.audio_capture.cleanup()
        
        if self.audio_preprocessing:
            self.audio_preprocessing.cleanup()
        
        if self.speech_to_text:
            self.speech_to_text.cleanup()
        
        if self.subtitle_renderer:
            self.subtitle_renderer.cleanup()
