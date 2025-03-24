# modules/subtitle_renderer.py
import tkinter as tk
import threading
import time
from typing import List, Dict, Optional

class SubtitleRenderer:
    def __init__(self, config=None):
        """Initialize subtitle renderer."""
        self.config = config or {}
        self.fade_timeout = self.config.get('fade_timeout', 5.0)  # seconds
        self.max_lines = self.config.get('max_lines', 2)
        self.font_size = self.config.get('font_size', 18)
        self.font_family = self.config.get('font_family', 'Arial')
        
        self.subtitles = []
        self.fade_timer = None
        
        # Initialize UI elements
        self.root = None
        self.subtitle_frame = None
        self.subtitle_labels = []
        
        # Thread safety
        self.lock = threading.Lock()
    
    def initialize(self, parent_window=None):
        """Initialize the subtitle renderer UI."""
        try:
            if parent_window:
                # Use provided parent window
                self.root = parent_window
            else:
                # Create a new window
                self.root = tk.Tk()
                self.root.title("Subtitle Overlay")
                self.root.geometry("800x200")
                self.root.attributes("-topmost", True)
                self.root.configure(bg='black')
                self.root.withdraw()  # Hide window until needed
            
            # Create subtitle frame
            self.subtitle_frame = tk.Frame(self.root, bg='black')
            self.subtitle_frame.pack(fill=tk.BOTH, expand=True)
            
            # Create subtitle labels
            for i in range(self.max_lines):
                label = tk.Label(
                    self.subtitle_frame,
                    text="",
                    font=(self.font_family, self.font_size),
                    fg="white",
                    bg="black",
                    wraplength=780
                )
                label.pack(fill=tk.X, pady=2)
                self.subtitle_labels.append(label)
            
            return True
        
        except Exception as e:
            print(f"Error initializing subtitle renderer: {str(e)}")
            return False
    
    def show_subtitle(self, text: str, speaker: Optional[str] = None):
        """Show a subtitle with optional speaker attribution."""
        with self.lock:
            # Clear any existing fade timeout
            if self.fade_timer:
                self.root.after_cancel(self.fade_timer)
                self.fade_timer = None
            
            # Add new subtitle to the queue
            subtitle = {
                'text': text,
                'speaker': speaker,
                'timestamp': time.time()
            }
            
            self.subtitles.append(subtitle)
            
            # Keep only the latest subtitles based on maxLines
            if len(self.subtitles) > self.max_lines:
                self.subtitles = self.subtitles[-self.max_lines:]
            
            # Update the subtitle display
            self.update_subtitle_display()
            
            # Show window if it was hidden
            if not parent_window and self.root.state() == 'withdrawn': # type: ignore
                self.root.deiconify()
            
            # Set fade timeout
            self.fade_timer = self.root.after(
                int(self.fade_timeout * 1000),
                self.fade_oldest_subtitle
            )
    
    def fade_oldest_subtitle(self):
        """Remove the oldest subtitle from display."""
        with self.lock:
            if self.subtitles:
                self.subtitles.pop(0)
                self.update_subtitle_display()
                
                if self.subtitles:
                    # Schedule next fade if there are still subtitles
                    self.fade_timer = self.root.after(
                        int(self.fade_timeout * 1000),
                        self.fade_oldest_subtitle
                    )
                else:
                    self.fade_timer = None
                    # Hide window if empty
                    if not parent_window: # type: ignore
                        self.root.withdraw()
    
    def update_subtitle_display(self):
        """Update the subtitle display with current subtitles."""
        # Clear all labels
        for label in self.subtitle_labels:
            label.config(text="")
        
        # Fill with current subtitles
        for i, subtitle in enumerate(self.subtitles):
            if i < len(self.subtitle_labels):
                if subtitle['speaker']:
                    display_text = f"{subtitle['speaker']}: {subtitle['text']}"
                else:
                    display_text = subtitle['text']
                self.subtitle_labels[i].config(text=display_text)
    
    def clear(self):
        """Clear all subtitles."""
        with self.lock:
            self.subtitles = []
            self.update_subtitle_display()
            
            if self.fade_timer:
                self.root.after_cancel(self.fade_timer)
                self.fade_timer = None
            
            if not parent_window: # type: ignore
                self.root.withdraw()
    
    def cleanup(self):
        """Clean up resources."""
        self.clear()
        if self.root and not parent_window: # type: ignore
            self.root.destroy()
