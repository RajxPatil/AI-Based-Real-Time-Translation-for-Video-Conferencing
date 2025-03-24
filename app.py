# app.py
import os
import tkinter as tk
from tkinter import ttk
import threading
import time
from modules.realtime_subtitle_system import RealTimeSubtitleSystem

class SubtitleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Subtitle System")
        self.root.geometry("800x600")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("TLabel", font=("Arial", 12))
        
        # Create frame for controls
        self.control_frame = ttk.Frame(root, padding=10)
        self.control_frame.pack(fill=tk.X)
        
        # Start/Stop buttons
        self.start_button = ttk.Button(
            self.control_frame, 
            text="Start Subtitles", 
            command=self.start_system
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            self.control_frame, 
            text="Stop Subtitles", 
            command=self.stop_system,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Language selection
        ttk.Label(self.control_frame, text="Target Language:").pack(side=tk.LEFT, padx=10)
        
        self.language_var = tk.StringVar(value="en")
        self.language_combo = ttk.Combobox(
            self.control_frame,
            textvariable=self.language_var,
            values=["en", "es", "fr", "de", "ja", "zh-Hans"],
            width=10
        )
        self.language_combo.pack(side=tk.LEFT, padx=5)
        self.language_combo.bind("<<ComboboxSelected>>", self.change_language)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            self.control_frame, 
            textvariable=self.status_var,
            font=("Arial", 12)
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # Create the subtitle system
        self.subtitle_system = RealTimeSubtitleSystem({
            'speech_key': os.environ.get('AZURE_SPEECH_KEY'),
            'speech_region': os.environ.get('AZURE_SPEECH_REGION'),
            'translator_key': os.environ.get('AZURE_TRANSLATOR_KEY'),
            'translator_region': os.environ.get('AZURE_TRANSLATOR_REGION'),
            'language_key': os.environ.get('AZURE_LANGUAGE_KEY'),
            'language_endpoint': os.environ.get('AZURE_LANGUAGE_ENDPOINT'),
            'default_language': 'en',
            'target_language': 'en'
        })
        
        # Initialize in a separate thread to avoid blocking the UI
        self.init_thread = threading.Thread(target=self.initialize_system)
        self.init_thread.daemon = True
        self.init_thread.start()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def initialize_system(self):
        """Initialize the subtitle system."""
        self.status_var.set("Initializing...")
        success = self.subtitle_system.initialize()
        if success:
            self.status_var.set("Ready")
        else:
            self.status_var.set("Initialization failed")
    
    def start_system(self):
        """Start the subtitle system."""
        self.status_var.set("Starting...")
        success = self.subtitle_system.start()
        
        if success:
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_var.set("Running")
        else:
            self.status_var.set("Start failed")
    
    def stop_system(self):
        """Stop the subtitle system."""
        self.status_var.set("Stopping...")
        success = self.subtitle_system.stop()
        
        if success:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_var.set("Stopped")
        else:
            self.status_var.set("Stop failed")
    
    def change_language(self, event=None):
        """Change the target language."""
        language = self.language_var.get()
        self.subtitle_system.set_target_language(language)
        self.status_var.set(f"Language changed to {language}")
    
    def on_close(self):
        """Handle window close event."""
        if self.subtitle_system:
            self.subtitle_system.cleanup()
        self.root.destroy()

if __name__ == "__main__":
    # Set up environment variables for testing
    # In production, these would be set in the environment
    if not os.environ.get('AZURE_SPEECH_KEY'):
        os.environ['AZURE_SPEECH_KEY'] = 'your-azure-speech-key'
    if not os.environ.get('AZURE_SPEECH_REGION'):
        os.environ['AZURE_SPEECH_REGION'] = 'your-azure-region'
    if not os.environ.get('AZURE_TRANSLATOR_KEY'):
        os.environ['AZURE_TRANSLATOR_KEY'] = 'your-azure-translator-key'
    if not os.environ.get('AZURE_TRANSLATOR_REGION'):
        os.environ['AZURE_TRANSLATOR_REGION'] = 'your-azure-region'
    if not os.environ.get('AZURE_LANGUAGE_KEY'):
        os.environ['AZURE_LANGUAGE_KEY'] = 'your-azure-language-key'
    if not os.environ.get('AZURE_LANGUAGE_ENDPOINT'):
        os.environ['AZURE_LANGUAGE_ENDPOINT'] = 'https://your-language-resource.cognitiveservices.azure.com'
    
    root = tk.Tk()
    app = SubtitleApp(root)
    root.mainloop()
