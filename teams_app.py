import tkinter as tk
from tkinter import ttk, simpledialog
import os
import threading
from dotenv import load_dotenv # type: ignore
from teams_integration import TeamsIntegration

load_dotenv()

class TeamsSubtitleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Teams Subtitle System")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("TLabel", font=("Arial", 12))
        
        # Create frame for meeting controls
        self.meeting_frame = ttk.LabelFrame(root, text="Teams Meeting", padding=10)
        self.meeting_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Meeting link entry
        ttk.Label(self.meeting_frame, text="Meeting Link:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.meeting_link_var = tk.StringVar()
        self.meeting_link_entry = ttk.Entry(
            self.meeting_frame, 
            textvariable=self.meeting_link_var,
            width=50
        )
        self.meeting_link_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        
        # Join/Leave buttons
        self.join_button = ttk.Button(
            self.meeting_frame, 
            text="Join Meeting", 
            command=self.join_meeting
        )
        self.join_button.grid(row=1, column=1, padx=5, pady=10)
        
        self.leave_button = ttk.Button(
            self.meeting_frame, 
            text="Leave Meeting", 
            command=self.leave_meeting,
            state=tk.DISABLED
        )
        self.leave_button.grid(row=1, column=2, padx=5, pady=10)
        
        # Create frame for subtitle controls
        self.subtitle_frame = ttk.LabelFrame(root, text="Subtitle Settings", padding=10)
        self.subtitle_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Language selection
        ttk.Label(self.subtitle_frame, text="Target Language:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.language_var = tk.StringVar(value="en")
        self.language_combo = ttk.Combobox(
            self.subtitle_frame,
            textvariable=self.language_var,
            values=["en", "es", "fr", "de", "ja", "zh-Hans"],
            width=10
        )
        self.language_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.language_combo.bind("<<ComboboxSelected>>", self.change_language)
        
        # Status label
        self.status_frame = ttk.Frame(root, padding=10)
        self.status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.status_var = tk.StringVar(value="Not connected")
        self.status_label = ttk.Label(
            self.status_frame, 
            textvariable=self.status_var,
            font=("Arial", 12)
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Create the Teams integration
        self.teams_integration = TeamsIntegration()
        
        # Initialize in a separate thread
        self.init_thread = threading.Thread(target=self.initialize_integration)
        self.init_thread.daemon = True
        self.init_thread.start()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def initialize_integration(self):
        """Initialize the Teams integration."""
        self.status_var.set("Initializing...")
        success = self.teams_integration.initialize()
        if success:
            self.status_var.set("Ready to join meeting")
        else:
            self.status_var.set("Initialization failed")
    
    def join_meeting(self):
        """Join Teams meeting."""
        meeting_link = self.meeting_link_var.get()
        if not meeting_link:
            self.status_var.set("Please enter a meeting link")
            return
        
        self.status_var.set("Joining meeting...")
        
        # Join meeting in a separate thread to avoid UI freezing
        def join_thread():
            success = self.teams_integration.join_meeting(meeting_link)
            if success:
                self.root.after(0, lambda: self.join_button.config(state=tk.DISABLED))
                self.root.after(0, lambda: self.leave_button.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.status_var.set("Connected to meeting"))
            else:
                self.root.after(0, lambda: self.status_var.set("Failed to join meeting"))
        
        thread = threading.Thread(target=join_thread)
        thread.daemon = True
        thread.start()
    
    def leave_meeting(self):
        """Leave Teams meeting."""
        self.status_var.set("Leaving meeting...")
        self.teams_integration.leave_meeting()
        
        self.join_button.config(state=tk.NORMAL)
        self.leave_button.config(state=tk.DISABLED)
        self.status_var.set("Disconnected from meeting")
    
    def change_language(self, event=None):
        """Change the target language for subtitles."""
        language = self.language_var.get()
        self.teams_integration.set_target_language(language)
        self.status_var.set(f"Target language set to {language}")
    
    def on_close(self):
        """Handle window close event."""
        if self.teams_integration:
            self.teams_integration.cleanup()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TeamsSubtitleApp(root)
    root.mainloop()
