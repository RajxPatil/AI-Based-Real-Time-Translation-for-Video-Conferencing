# modules/audio_capture.py
import pyaudio # type: ignore
import numpy as np # type: ignore
import threading
import queue
import time
from typing import Callable, Optional

class AudioCapture:
    def __init__(self, config=None):
        """Initialize audio capture with specified configuration."""
        self.config = config or {}
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000  # 16kHz is common for speech recognition
        self.chunk = 1024  # Number of frames per buffer
        
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.audio_callback = None
        self.recording_thread = None
        
        # For Teams integration
        self.teams_audio_stream = None
        self.teams_audio_thread = None
    
    def initialize_microphone_capture(self) -> bool:
        """Initialize microphone for audio capture."""
        try:
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
                stream_callback=self._audio_callback
            )
            return True
        except Exception as e:
            print(f"Error initializing microphone: {str(e)}")
            return False
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Internal callback for audio data processing."""
        if self.is_recording:
            self.audio_queue.put(in_data)
            if self.audio_callback:
                # Convert to numpy array for processing
                audio_data = np.frombuffer(in_data, dtype=np.int16)
                self.audio_callback(audio_data)
        return (in_data, pyaudio.paContinue)
    
    def set_audio_callback(self, callback: Callable):
        """Set callback function for audio data."""
        self.audio_callback = callback
    
    def start_recording(self):
        """Start audio recording."""
        if self.stream and not self.is_recording:
            self.is_recording = True
            self.stream.start_stream()
            self.recording_thread = threading.Thread(target=self._process_audio_queue)
            self.recording_thread.daemon = True
            self.recording_thread.start()
            return True
        return False
    
    def _process_audio_queue(self):
        """Process audio data from queue in a separate thread."""
        while self.is_recording:
            try:
                # Just dequeue if no callback is set
                # The _audio_callback already handles the callback
                self.audio_queue.get(timeout=0.1)
                self.audio_queue.task_done()
            except queue.Empty:
                continue
    
    def stop_recording(self):
        """Stop audio recording."""
        if self.stream and self.is_recording:
            self.is_recording = False
            self.stream.stop_stream()
            if self.recording_thread and self.recording_thread.is_alive():
                self.recording_thread.join(timeout=1.0)
            return True
        return False
    
    def initialize_teams_capture(self, teams_audio_stream=None):
        """Initialize capture from Microsoft Teams."""
        self.teams_audio_stream = teams_audio_stream
        
        if self.teams_audio_stream:
            # Start a thread to read from Teams audio stream
            self.teams_audio_thread = threading.Thread(target=self._process_teams_audio)
            self.teams_audio_thread.daemon = True
            self.teams_audio_thread.start()
            return True
        return False
    
    def _process_teams_audio(self):
        """Process audio data from Teams in a separate thread."""
        while self.teams_audio_stream and self.is_recording:
            try:
                # This is a placeholder for reading from Teams audio stream
                # In a real implementation, you would read from the actual Teams API
                audio_data = self.teams_audio_stream.read(self.chunk)
                
                if audio_data and self.audio_callback:
                    # Convert to numpy array for processing
                    audio_np = np.frombuffer(audio_data, dtype=np.int16)
                    self.audio_callback(audio_np)
                    
                time.sleep(0.01)  # Small delay to prevent CPU hogging
            except Exception as e:
                print(f"Error processing Teams audio: {str(e)}")
                time.sleep(0.1)
    
    def cleanup(self):
        """Clean up resources."""
        if self.stream:
            self.stop_recording()
            self.stream.close()
        self.audio.terminate()
        
        # Stop Teams audio processing
        if self.teams_audio_thread and self.teams_audio_thread.is_alive():
            self.is_recording = False
            self.teams_audio_thread.join(timeout=1.0)
