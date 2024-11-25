import tkinter as tk
from tkinter import filedialog
import simpleaudio as sa
import os
import pygame

class AudioPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Player")
        self.root.geometry("300x200")

        self.audio_file = None
        self.playback_object = None
        self.is_playing = False  # Track if audio is playing
        self.is_paused = False    # Track if audio is paused

        self.setup_ui()

    def setup_ui(self):
        self.load_button = tk.Button(self.root, text="Load Audio File", command=self.load_audio_file)
        self.load_button.pack(pady=20)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_audio, state=tk.DISABLED)
        self.play_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_audio, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.status_label = tk.Label(self.root, text="Status: Ready")
        self.status_label.pack(pady=20)

    def load_audio_file(self):
        """Load a single audio file."""
        self.audio_file = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.wav;*.mp3;*.flac")],
            title="Select an Audio File"
        )
        if self.audio_file:
            self.play_button.config(state=tk.NORMAL)
            self.status_label.config(text=f"Loaded: {os.path.basename(self.audio_file)}")

    def play_audio(self):
        """Play the loaded audio file."""
        if self.audio_file:
            if self.audio_file.endswith('.wav'):
                wave_obj = sa.WaveObject.from_wave_file(self.audio_file)
                self.playback_object = wave_obj.play()
                self.is_playing = True
                self.is_paused = False
            elif self.audio_file.endswith('.mp3'):
                pygame.mixer.init()
                pygame.mixer.music.load(self.audio_file)
                pygame.mixer.music.play()
                self.is_playing = True
                self.is_paused = False
            
            self.play_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text=f"Playing: {os.path.basename(self.audio_file)}")

    def stop_audio(self):
        """Stop the audio playback."""
        if self.audio_file:
            if self.audio_file.endswith('.wav'):
                if self.playback_object is not None:
                    self.playback_object.stop()
                    self.is_playing = False
            elif self.audio_file.endswith('.mp3'):
                pygame.mixer.music.stop()
                self.is_playing = False

            self.status_label.config(text="Stopped")
            self.play_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioPlayerApp(root)
    root.mainloop()
