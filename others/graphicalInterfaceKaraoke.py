import tkinter as tk
from tkinter import Menu
from tkinter import ttk, filedialog, messagebox, Listbox
import csv
import os 
import shutil
import pygame
import simpleaudio as sa
import re
import time 
import threading
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from KaraokeToolBox import Treator

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.title("Karaoke App")
        self.geometry("600x400")
        self.minsize(400, 300)

        # Define core paths and ensure directories
        self.setup_directories()

        # Initialize attributes and events
        self.current_song = None
        self.karaoke_on_play = None
        self.recording_stop_event = threading.Event()
        self.karaoke_stop_event = threading.Event()
        self.scene_history = []

        # Setup main UI components
        self.create_menu()
        self.frame = None
        self.show_main_menu()

    def setup_directories(self):
        """Set up required directories."""
        root_path = os.getcwd()
        self.dirs = {
            "audio": os.path.join(root_path, "data", "mp3"),
            "lrc": os.path.join(root_path, "data", "LRCFiles"),
            "spleeter": os.path.join(root_path, "data", "spleeter"),
            "record": os.path.join(root_path, "data", "record")
        }
        for directory in self.dirs.values():
            os.makedirs(directory, exist_ok=True)

    def create_menu(self):
        """Create the menu bar."""
        menu_bar = Menu(self)
        
        # Menu Items
        menu = Menu(menu_bar, tearoff=0)
        menu.add_command(label="Play", command=self.show_play_scene)
        menu.add_command(label="Learn", command=self.show_learn_scene)
        menu_bar.add_cascade(label="Menu", menu=menu)
        
        # Additional Menu Commands
        menu_bar.add_command(label="Score Board", command=lambda: self.show_csv_table("Score"))
        menu_bar.add_command(label="Add Song", command=self.show_add_song_menu)
        menu_bar.add_command(label="Help", command=self.show_help_scene)
        menu_bar.add_command(label="Back", command=self.go_back)
        self.config(menu=menu_bar)

    def show_help_scene(self):
        """Display the main menu."""
        self.clear_frame()
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Main Menu Label and Buttons
        tk.Label(self.frame, text="Karaoke App!", font=("Arial", 24)).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.frame, text="Play", command=self.show_play_scene).grid(row=1, column=0, pady=5)
        tk.Button(self.frame, text="Learn", command=self.show_learn_scene).grid(row=2, column=0, pady=5)

        self.scene_history.append(self.show_main_menu)

    def go_back(self):
        """Navigate back in history if possible."""
        if len(self.scene_history) > 1:
            self.scene_history.pop()
            self.scene_history[-1]()

    def clear_frame(self):
        """Clear the current frame."""
        if self.frame:
            self.frame.destroy()

    def show_main_menu(self):
        """Display the main menu."""
        self.clear_frame()
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Main Menu Label and Buttons
        tk.Label(self.frame, text="Karaoke App!", font=("Arial", 24)).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.frame, text="Play", command=self.show_play_scene).grid(row=1, column=0, pady=5)
        tk.Button(self.frame, text="Learn", command=self.show_learn_scene).grid(row=2, column=0, pady=5)

        self.scene_history.append(self.show_main_menu)

    def show_play_scene(self):
        """Display the play scene where users can select songs."""
        self.clear_frame()
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Song Selection Label
        tk.Label(self.frame, text="Select a song to start", font=("Arial", 18)).grid(row=0, column=0, padx=10, pady=10)

        # Display available songs
        for i, song in enumerate(os.listdir(self.dirs["audio"]), start=1):
            song_name = os.path.splitext(song)[0]
            tk.Button(self.frame, text=song_name, command=lambda s=song_name: self.song_selected(s)).grid(row=i, column=0, pady=2)

        self.scene_history.append(self.show_play_scene)

    def song_selected(self, song_name):
        """Ask if the user wants to preview the song before karaoke."""
        response = messagebox.askyesno("Selected Song", f"Would you like to listen to '{song_name}' first?")
        if response:
            self.show_preview_scene(song_name)
        else:
            self.start_karaoke(song_name)

    def show_preview_scene(self, song_name):
        """Preview selected song before starting karaoke."""
        self.clear_frame()
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Play, Stop, and Start Buttons
        tk.Button(self.frame, text="Play", command=lambda: self.play_audio(song_name)).grid(row=1, column=0, pady=10)
        tk.Button(self.frame, text="Stop", command=self.stop_audio).grid(row=1, column=1, pady=10)
        tk.Button(self.frame, text="Start Karaoke", command=lambda: self.start_karaoke(song_name)).grid(row=2, column=0, columnspan=2, pady=10)

    def play_audio(self, song_name):
        """Play the selected song."""
        audio_path = os.path.join(self.dirs["audio"], song_name + '.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

    def stop_audio(self):
        """Stop the currently playing audio."""
        pygame.mixer.music.stop()

    def parse_lyrics(self, lrc_file_path):
        """Parse .lrc file and return lyrics with timestamps."""
        lyrics = []
        with open(lrc_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(r'\[(\d{2}):(\d{2}\.\d{2})\](.*)', line)
                if match:
                    minutes, seconds, lyric = int(match.group(1)), float(match.group(2)), match.group(3).strip()
                    timestamp = minutes * 60 + seconds
                    lyrics.append({"timestamp": timestamp, "lyric": lyric})
        return lyrics

    def start_karaoke(self, song_name):
        """Start the karaoke session."""
        self.current_song = song_name
        self.show_karaoke_scene()
        self.play_karaoke_song(song_name)

    def show_karaoke_scene(self):
        """Display the karaoke scene."""
        self.clear_frame()
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.lyrics_label = tk.Label(self.frame, font=("Arial", 18), width=60, height=10)
        self.lyrics_label.grid(row=1, column=0, pady=20)

        self.progress_bar = ttk.Progressbar(self.frame, length=400, mode='determinate')
        self.progress_bar.grid(row=2, column=0, pady=10)

        self.stop_button = tk.Button(self.frame, text="Stop", command=self.stop_karaoke)
        self.stop_button.grid(row=3, column=0, pady=10)

    def play_karaoke_song(self, song_name):
        """Play karaoke song with lyrics display."""
        song_path = os.path.join(self.dirs["spleeter"], song_name, f"{song_name}_accompaniment.wav")
        lyrics_path = os.path.join(self.dirs["lrc"], f"{song_name}.lrc")

        # Load lyrics and initialize music
        self.lyrics_data = self.parse_lyrics(lyrics_path)
        pygame.mixer.init()
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        self.update_lyrics()

    def update_lyrics(self):
        """Update lyrics on screen according to the timestamp."""
        while pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() / 1000  # Get current time in seconds
            for lyric in self.lyrics_data:
                if lyric["timestamp"] <= current_time:
                    self.lyrics_label.config(text=lyric["lyric"])
            time.sleep(0.1)

    def stop_karaoke(self):
        """Stop the karaoke session."""
        pygame.mixer.music.stop()

    def show_add_song_menu(self):
        """Display scene to add new songs."""
        self.clear_frame()
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(self.frame, text="Add New Song", font=("Arial", 16)).grid(row=0, column=0, pady=10)
        tk.Button(self.frame, text="With Lyrics", command=self.add_song_with_lyrics).grid(row=1, column=0, pady=5)
        tk.Button(self.frame, text="Without Lyrics", command=self.add_song_only).grid(row=2, column=0, pady=5)
        
    def start_score_compute(self, record):
        """Display content for Scene 2B."""
        if self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        label = tk.Label(self.frame, text="Welcome to Scene 2B", font=("Arial", 24))
        label.grid(row=0, column=0, padx=10, pady=10)

        self.scene_history.append(self.show_learn_scene)

    def show_learn_scene(self):
        """Display content for Scene 2B."""
        if self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        label = tk.Label(self.frame, text="Welcome to Scene 2B", font=("Arial", 24))
        label.grid(row=0, column=0, padx=10, pady=10)

        self.scene_history.append(self.show_learn_scene)
        
    def show_csv_table(self, sort_by):
        if self.frame:
            self.frame.destroy()
        
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")  
        
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(self.frame, show="headings")
        
        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.load_csv_data("data/sample_data.csv", sort_by)
        
        self.tree.grid(row=0, column=0, sticky="nsew")  
        vsb.grid(row=0, column=1, sticky="ns")  
        hsb.grid(row=1, column=0, sticky="ew")  
        
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.scene_history.append(self.show_csv_table)

    def load_csv_data(self, filepath, sort_by):
        try:
            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  
                
                self.tree["columns"] = ["Rank"] + headers
                self.tree.heading("Rank", text="Rank")
                self.tree.column("Rank", width=50, anchor="center")
                
                for header in headers:
                    self.tree.heading(header, text=header)
                    self.tree.column(header, width=100, anchor="center")
                
                rows = list(reader)

                if sort_by in headers:
                    sort_index = headers.index(sort_by)
                    rows.sort(key=lambda x: float(x[sort_index]) if x[sort_index].replace('.', '', 1).isdigit() else x[sort_index], reverse=True)
                
                for index, row in enumerate(rows):
                    rank = index + 1
                    self.tree.insert("", "end", values=(rank, *row))

        except Exception as e:
            print(f"Error loading CSV file: {e}")

    def add_new_song_with_lrc(self):
        if self.frame:
            self.frame.destroy()
            
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        # Song Name Entry
        song_name_label = tk.Label(self.frame, text="Enter Song Name:")
        song_name_label.grid(row=0, column=0, pady=10, padx=10)
        
        song_name_entry = tk.Entry(self.frame)
        song_name_entry.grid(row=1, column=0, pady=5)

        # Audio File Selection
        audio_button = tk.Button(self.frame, text="Browse Audio File", command=lambda: self.browse_file(song_name_entry, 'audio'))
        audio_button.grid(row=2, column=0, pady=10)

        # Lyrics File Selection
        lrc_button = tk.Button(self.frame, text="Browse Lyrics File", command=lambda: self.browse_file(song_name_entry, 'lrc'))
        lrc_button.grid(row=3, column=0, pady=10)

        # Out Selection
        out_button = tk.Button(self.frame, text="Finish", command=self.show_Menu)
        out_button.grid(row=4, column=0, pady=10)

        self.scene_history.append(self.add_new_song_with_lrc)
    
    def add_new_song_only(self):
        if self.frame:
            self.frame.destroy()
            
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        # Song Name Entry
        song_name_label = tk.Label(self.frame, text="Enter Song Name:")
        song_name_label.grid(row=0, column=0, pady=10, padx=10)
        
        song_name_entry = tk.Entry(self.frame)
        song_name_entry.grid(row=1, column=0, pady=5)

        # Audio File Selection
        audio_button = tk.Button(self.frame, text="Browse Audio File", command=lambda: self.browse_file(song_name_entry, 'audio'))
        audio_button.grid(row=2, column=0, pady=10)

        # Out Selection
        out_button = tk.Button(self.frame, text="Finish", command=self.show_Menu)
        out_button.grid(row=3, column=0, pady=10)

        self.scene_history.append(self.add_new_song_only)


    def add_lrc_only(self):
        if self.frame:
            self.frame.destroy()
            
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        # Song Name Entry
        song_name_label = tk.Label(self.frame, text="Enter Song Name:")
        song_name_label.grid(row=0, column=0, pady=10, padx=10)
        
        song_name_entry = tk.Entry(self.frame)
        song_name_entry.grid(row=1, column=0, pady=5)

        # LRC File Selection
        lrc_button = tk.Button(self.frame, text="Browse Lyrics File", command=lambda: self.browse_file(None, 'lrc'))
        lrc_button.grid(row=2, column=0, pady=10)

        # Out Selection
        out_button = tk.Button(self.frame, text="Finish", command=self.show_Menu)
        out_button.grid(row=3, column=0, pady=10)

        self.scene_history.append(self.add_lrc_only)
    
    def browse_file(self, song_name_entry, file_type):
        filetypes = [("Audio Files", "*.mp3 *.wav")] if file_type == 'audio' else [("LRC Files", "*.lrc")]
        file = filedialog.askopenfilename(title=f"Select {file_type.capitalize()} File", filetypes=filetypes)

        if not file:  # If no file is selected
            messagebox.showwarning(f"No {file_type.capitalize()} File", f"No {file_type.capitalize()} file selected.")
            return
            
        # Get the song name and ensure it is entered
        song_name = song_name_entry.get().strip()
        if not song_name:
            messagebox.showwarning("Missing Song Name", "Please enter a song name before selecting the files.")
            return

        # Save the selected files into respective directories
        try:
            # Construct the file names using the song name and move the files
            base_name = song_name.replace(" ", "_").lower()  # Sanitizing the song name for filenames
            audio_dest = os.path.join(self.audio_dir, f"{base_name}{os.path.splitext(file)[1]}")
            lrc_dest = os.path.join(self.lrc_dir, f"{base_name}.lrc")

            if file_type == 'audio':
                shutil.copy(file, audio_dest)
                messagebox.showinfo("Song Added", f"Audio file for '{song_name}' added successfully!")
            elif file_type == 'lrc':
                shutil.copy(file, lrc_dest)
                messagebox.showinfo("Song Added", f"LRC file for '{song_name}' added successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error saving files: {e}")

if __name__ == "__main__":

    print(os.getcwd())
    app = Application()
    app.mainloop()