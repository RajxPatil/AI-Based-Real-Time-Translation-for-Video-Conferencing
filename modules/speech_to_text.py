# modules/speech_to_text.py
import azure.cognitiveservices.speech as speechsdk # type: ignore
import threading
from typing import Callable, Dict, Optional

class SpeechToText:
    def __init__(self, config):
        """Initialize Speech-to-Text with Azure Speech Services."""
        self.api_key = config.get('api_key')
        self.region = config.get('region')
        self.default_language = config.get('default_language', 'en-US')
        
        # Initialize speech config
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.api_key, 
            region=self.region
        )
        self.speech_config.speech_recognition_language = self.default_language
        
        # Enable continuous recognition
        self.speech_config.enable_dictation()
        
        # Initialize recognizer
        self.recognizer = None
        self.is_recognizing = False
        self.transcription_callback = None
        
        # Language mapping
        self.language_map = {
            'en': 'en-US',
            'es': 'es-ES',
            'fr': 'fr-FR',
            'de': 'de-DE',
            'ja': 'ja-JP',
            'zh': 'zh-CN',
            # Add more mappings as needed
        }
    
    def set_language(self, language_code: str):
        """Set the language for speech recognition."""
        if self.recognizer:
            self.stop_recognition()
        
        # Convert ISO 639-1 to language-region format if needed
        full_language_code = self.language_map.get(language_code, language_code)
        self.speech_config.speech_recognition_language = full_language_code
        print(f"Speech recognition language set to: {full_language_code}")
    
    def start_recognition(self, audio_config=None):
        """Start continuous speech recognition."""
        if self.is_recognizing:
            self.stop_recognition()
        
        # If no audio config provided, use default microphone
        if not audio_config:
            audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        
        # Create recognizer
        self.recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, 
            audio_config=audio_config
        )
        
        # Set up callbacks
        self.recognizer.recognizing.connect(self._recognizing_callback)
        self.recognizer.recognized.connect(self._recognized_callback)
        self.recognizer.canceled.connect(self._canceled_callback)
        self.recognizer.session_stopped.connect(self._session_stopped_callback)
        
        # Start continuous recognition
        self.recognizer.start_continuous_recognition()
        self.is_recognizing = True
        print("Speech recognition started")
    
    def _recognizing_callback(self, event):
        """Callback for interim recognition results."""
        if self.transcription_callback:
            self.transcription_callback({
                'text': event.result.text,
                'is_final': False,
                'language_code': self.speech_config.speech_recognition_language
            })
    
    def _recognized_callback(self, event):
        """Callback for final recognition results."""
        if (event.result.reason == speechsdk.ResultReason.RecognizedSpeech and 
            self.transcription_callback):
            self.transcription_callback({
                'text': event.result.text,
                'is_final': True,
                'language_code': self.speech_config.speech_recognition_language
            })
    
    def _canceled_callback(self, event):
        """Callback for recognition cancellation."""
        print(f"Speech recognition canceled: {event.cancellation_details.reason}")
        if event.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {event.cancellation_details.error_details}")
        self.is_recognizing = False
    
    def _session_stopped_callback(self, event):
        """Callback for session stop."""
        print("Speech recognition session stopped")
        self.is_recognizing = False
    
    def set_transcription_callback(self, callback: Callable):
        """Set callback function for transcription results."""
        self.transcription_callback = callback
    
    def stop_recognition(self):
        """Stop continuous speech recognition."""
        if self.recognizer and self.is_recognizing:
            self.recognizer.stop_continuous_recognition()
            self.is_recognizing = False
            print("Speech recognition stopped")
    
    def cleanup(self):
        """Clean up resources."""
        if self.recognizer:
            self.stop_recognition()
            self.recognizer = None
