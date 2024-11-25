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
import uuid
import random
import ingescape as igs
import json

from whiteBordUtils import *

class Application(tk.Tk):

    def list_files_by_subdirectory(self, parent_directory):
        # Initialize the dictionary
        directory_files = {}
        
        # Iterate through all subdirectories in the parent directory
        for root, dirs, files in os.walk(parent_directory):
            # Skip the parent directory itself
            if root == parent_directory:
                continue
            # Extract the subdirectory name
            subdir = os.path.basename(root)
            # Add the list of files as the value
            directory_files[subdir] = files
        
        return directory_files

    def __init__(self, tretor, whiteboard): 
        super().__init__()
        
        # Set window title and size
        self.title("karaoke-ingescape-v1.0")
        self.geometry("800x500")
        self.minsize(600, 500)  

        # Useful attributes 
        self.karaoke_on_play_song = None
        self.canvas = None
        self.recording = None
        self.recording_thread = None
        self.karaoke_thread = None
        self.recording_stop_event = threading.Event()
        self.karaoke_stop_event = threading.Event()
        self.is_running = False
        self.lyrics_data = []
        self.treator = tretor
        self.whiteboard = whiteboard
        
        self.root_path = os.getcwd()
        self.audio_dir = os.path.join(self.root_path, "data", "mp3")
        self.lrc_dir = os.path.join(self.root_path, "data", "LRCFiles")
        self.melodies_dir = os.path.join(self.root_path, "data", "melodies")
        self.waves_dir = os.path.join(self.root_path, "data", "wave")
        self.lyrics_dir = os.path.join(self.root_path, "data", "lyrics")
        self.spleeter_dir = os.path.join(self.root_path, "data", "spleeter")
        self.record_dir = os.path.join(self.root_path, "data", "record")
        self.icones_dir = os.path.join(self.root_path, "data", "icones")
        self.others_dir = os.path.join(self.root_path, "data", "others")

        # Ensure the directories exist
        os.makedirs(self.audio_dir, mode=0o777, exist_ok=True)
        os.makedirs(self.lrc_dir, mode=0o777, exist_ok=True)
        os.makedirs(self.melodies_dir, mode=0o777, exist_ok=True)
        os.makedirs(self.waves_dir, mode=0o777, exist_ok=True)
        os.makedirs(self.lyrics_dir, mode=0o777, exist_ok=True)
        os.makedirs(self.spleeter_dir, mode=0o777, exist_ok=True)
        os.makedirs(self.record_dir, mode=0o777, exist_ok=True)
        os.makedirs(self.icones_dir, mode=0o777, exist_ok=True)
        os.makedirs(self.others_dir, mode=0o777, exist_ok=True)

        path_json_file = os.path.join(self.others_dir, "songs_info.json")
        self.songs_info = self.treator._load_song_infos(path_json_file)
        
        # Allow window to be resizable
        self.rowconfigure(0, weight=1)  # Allow row 0 to expand
        self.columnconfigure(0, weight=1)  # Allow column 0 to expand
        
        # Create a menu bar
        menu_bar = Menu(self)
        
        # Menu
        scene_menu = Menu(menu_bar, tearoff=0)
        
        # Submenu Menu
        menu_submenu = Menu(scene_menu, tearoff=0)
        menu_submenu.add_command(label="Play", command=self.show_select_category)
        menu_submenu.add_command(label="Learn", command=self.show_learn_alone)
        
        # Add Scenes Cascade to menu bar
        menu_bar.add_cascade(label="Menu", menu=menu_submenu)
    
        # Score Board
        menu_bar.add_command(label="Score Board", command=lambda: self.show_csv_table("Score"))

        # Add New Song
        add_menu = Menu(scene_menu, tearoff=0)
        add_menu.add_command(label="Add New Song With Lyrics File", command=self.add_new_song_with_lrc)
        add_menu.add_command(label="Add New Song", command=self.add_new_song_only)
        add_menu.add_command(label="Add New Lyrics File", command=self.add_lrc_only)

        menu_bar.add_cascade(label="Add New", menu=add_menu)
        
        # Back
        menu_bar.add_command(label="Back", command=self.go_back)
        self.scene_history = []
        
        # Attach the menu bar to the window
        self.config(menu=menu_bar)
        
        # Create a frame to switch scenes
        self.frame = None
        self.scene_history = []

        self.show_Menu()

    def show_Menu(self):
        """Display content for Main Menu"""
        if self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")  # Make frame responsive

        self.rowconfigure(0, weight=1)  # Allow frame to expand
        self.columnconfigure(0, weight=1)
        
        label = tk.Label(self.frame, text="Ingescape Karaoke App ! \n Play Now !", font=("Arial", 24))
        label.grid(row=0, column=0, padx=10, pady=10)  # Center label in frame

        button_play = tk.Button(self.frame, text="Play !", command=self.show_select_category)
        button_play.grid(row=1, column=0, pady=10)

        button_learn = tk.Button(self.frame, text="Learn !", command=self.show_learn_alone)
        button_learn.grid(row=1, column=3, pady=10)

        self.scene_history.append(self.show_Menu)
    
    def go_back(self):
        """Go back on Scene"""
        if len(self.scene_history) > 1:
            self.scene_history.pop()
            previous_sence = self.scene_history[-1]
            previous_sence()

    def show_select_category(self):
        if self.frame:
            self.frame.destroy()
        
        self.whiteboard.category_selection_Whiteboard_interface()

        # Create the main canvas and frame
        self.canvas = tk.Canvas(self)
        self.frame = ttk.Frame(self.canvas)

        self.karaoke_stop_event.clear() 
        self.recording_stop_event.clear() 

        # Configure the scrollbar and attach it to the canvas
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Position the canvas and scrollbar using grid
        self.scrollbar.grid(row=0, column=1, sticky="ns")  # Stick the scrollbar to the right vertically
        self.canvas.grid(row=0, column=0, sticky="nsew")   # Expand the canvas to fill space
        
        # Add a label at the top
        label = tk.Label(self.frame, text="Select a category of songs", font=("Arial", 24))
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        categories = self.list_files_by_subdirectory(self.audio_dir)

        for i, category in enumerate(categories, start=1):  # Start from row 1 as the label is in row 0
            button = tk.Button(self.frame, text=f"{category}", command=lambda i=category: self.show_play(i))
            button.grid(row=i, column=0, sticky="ew", pady=2, padx=5)  # Use grid with sticky "ew" to expand horizontally
        
        # Configure row and column weights for layout expansion
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)  # Ensure buttons expand within the frame

        self.scene_history.append(self.show_select_category)

    def show_play(self, category):
        """Display content for Scene Play."""

        self.category = category
        self.karaoke_stop_event.clear() 
        self.recording_stop_event.clear() 

        self.whiteboard.selection_of_song_Whiteboard_interface()
        
        # Create the main canvas and frame
        self.canvas = tk.Canvas(self)
        self.frame = ttk.Frame(self.canvas)
        
        # Configure the scrollbar and attach it to the canvas
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Position the canvas and scrollbar using grid
        self.scrollbar.grid(row=0, column=1, sticky="ns")  # Stick the scrollbar to the right vertically
        self.canvas.grid(row=0, column=0, sticky="nsew")   # Expand the canvas to fill space
        
        # Add a label at the top
        label = tk.Label(self.frame, text="Select a song to start", font=("Arial", 24))
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # Attach the frame to the canvas window for scrolling
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Add buttons for each song, using grid
        files = self.list_files_by_subdirectory(self.audio_dir)

        for i, file in enumerate(files[category], start=1):
            file_name = os.path.splitext(os.path.basename(file))[0]
            
            self.full_name = file_name
            if file_name in self.songs_info:
                self.full_name = self.songs_info[file_name]["ar"] + ' - ' + self.songs_info[file_name]["ti"]
            
            button = tk.Button(self.frame, text=f"{self.full_name}", command=lambda i=file_name: self.item_clicked(i))
            button.grid(row=i, column=0, sticky="ew", pady=2, padx=5)  # Use grid with sticky "ew" to expand horizontally
        
        # Configure row and column weights for layout expansion
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)  # Ensure buttons expand within the frame
        
        # Add this function to the scene history for navigation
        self.scene_history.append(self.show_play)
    
    def item_clicked(self, selected_item):
        self.full_name = selected_item
        if selected_item in self.songs_info and self.songs_info[selected_item] != {}:
            self.full_name = self.songs_info[selected_item]["ar"] + ' - ' + self.songs_info[selected_item]["ti"]

        response = messagebox.askyesno(f"You choosed the song {self.full_name}", "Would you like to listen to the song first ?")
        self.scene_history.append(self.show_play)
        if response:
            self.show_preview_and_karaoke(selected_item)
        else:
            self.start_karaoke(selected_item)

    def show_preview_and_karaoke(self, selected_item):
        """Display content for Preview."""
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        self.play_button = tk.Button(self.frame, text="Play", command=lambda file_name=selected_item: self.play_audio(file_name))
        self.play_button.grid(row=1, column=0, pady=10)

        self.stop_button = tk.Button(self.frame, text="Stop", command=self.stop_audio, state=tk.DISABLED)
        self.stop_button.grid(row=1, column=1, pady=10)

        self.status_label = tk.Label(self.frame, text="Status: Ready")
        self.status_label.grid(row=1, column=2, pady=10)

        self.start_karaoke_ = tk.Button(self.frame, text="Start !", command=lambda file_name=selected_item: self.start_karaoke(file_name))
        self.start_karaoke_.grid(row=2, column=1, pady=10)

        self.full_name = selected_item
        if selected_item in self.songs_info and self.songs_info[selected_item] != {}:
            self.full_name = self.songs_info[selected_item]["ar"] + ' - ' + self.songs_info[selected_item]["ti"]

        self.whiteboard.show_song_preview(selected_item, self.full_name)
    
    def play_audio(self, file_name):
        """Play the loaded audio file."""
        audio_file = os.path.join(self.waves_dir, file_name + '.wav')

        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        self.status_label.config(text="Playing")
        self.stop_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.DISABLED)
        self.start_karaoke_.config(state=tk.DISABLED)

    def stop_audio(self):
        """Stop the audio playback."""

        pygame.mixer.music.stop()
        self.status_label.config(text="Stopped")
        self.play_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.start_karaoke_.config(state=tk.NORMAL)
        
    
    def parse_lrc(self, lrc_file_path):
        lyrics_data = []
        try:
            with open(lrc_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    match = re.match(r'\[(\d{2}):(\d{2}\.\d{2})\](.*)', line)
                    if match:
                        minutes = int(match.group(1))
                        seconds = float(match.group(2))
                        lyric = match.group(3).strip()
                        timestamp = minutes * 60 + seconds
                        lyrics_data.append({"timestamp": timestamp, "lyric": lyric})
                        
            return lyrics_data
        
        except FileNotFoundError:
            print(f"Error: The file '{lrc_file_path}' was not found.")
        except Exception as e:
            print(f"Error: {e}")

    def start_recording(self, duration, output_path):
        """Start recording user voice for karaoke with better thread management and error handling."""
        sample_rate = 48000
        print("Recording...")
        try:
            self.recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=2,
                dtype='int32'
            )

            # Wait for the recording to finish or stop signal
            elapsed_time = 0
            while elapsed_time < duration and not self.recording_stop_event.is_set():
                time.sleep(0.1)
                elapsed_time += 0.1

            sd.stop()  # Ensure recording stops cleanly

            if not self.recording_stop_event.is_set():
                write(output_path, sample_rate, self.recording)
                print(f"Recording saved to {output_path}")
                self.start_score_compute(output_path)
            else:
                print("Recording was not saved.")
        except Exception as e:
            print(f"Error during recording: {e}")
        finally:
            self.recording = None

    def karaoke_loop(self):
        """Thread function to handle karaoke playback and lyric synchronization."""
        try:
            
            while pygame.mixer.music.get_busy() and not self.karaoke_stop_event.is_set():
                self.update_lyrics_display()
        except Exception as e:
            print(f"Error during karaoke loop: {e}")

    def update_lyrics_display(self):
        """Update lyrics and progress bar in the main thread."""
        current_time = pygame.mixer.music.get_pos() / 1000

        try:
            # Determine progress percentage
            song_duration = self.song_length
            progress = (current_time / song_duration) * 100

            # Schedule the update on the main thread
            self.after(0, self._update_ui_elements, current_time, progress)
        except Exception as e:
            print(f"Error updating lyrics display: {e}")

    def _update_ui_elements(self, current_time, progress):
        """Update UI elements (lyrics and progress bar) in a safe way."""
        try:
            self.progress_bar['value'] = progress
            for lyric in self.lyrics_data:
                if lyric["timestamp"] <= current_time:
                    self.lyrics_label.config(text=lyric["lyric"].replace(',', ',\n'))
        except Exception as e:
            print(f"Error updating UI elements: {e}")

    def start_karaoke(self, selected_item):
        """Display content for Karaoke with improved thread and event handling."""
        self.karaoke_stop_event.clear()
        self.recording_stop_event.clear()

        self.whiteboard.init_karaoke(self.full_name)
        self.whiteboard.show_lyrics()

        self.karaoke_on_play_song = selected_item
        self.lrc_file_path = os.path.join(self.lrc_dir, selected_item + '.lrc')

        response = messagebox.askyesno("Choose the difficulty", "Would you like to play in Hard difficulty?")
        if response:
            self.song_file_path = os.path.join(self.spleeter_dir, selected_item, selected_item + '_accompaniment.wav')
            self.level = 'Hard'
        else:
            self.song_file_path = os.path.join(self.waves_dir, selected_item + '.wav')
            self.level = 'Easy'

        self.recorded_output_path = os.path.join(self.record_dir, self.karaoke_on_play_song + str(uuid.uuid4()) + ".wav")

        try:
            self.lyrics_data = self.parse_lrc(self.lrc_file_path)
            self.lrcs = ""
            pygame.mixer.init()
            pygame.mixer.music.load(self.song_file_path)
            self.song_length = pygame.mixer.Sound(self.song_file_path).get_length()
        except Exception as e:
            print(f"Error loading karaoke resources: {e}")
            return

        # UI Initialization
        self.setup_karaoke_ui(selected_item)
        
        # Countdown before starting
        countdown_time = 5
        for i in range(countdown_time, 0, -1):
            self.countdown_label.config(text=f"Starting in {i}...")
            self.frame.update()
            time.sleep(1)

        self.countdown_label.config(text="Let's Sing!")
        self.frame.update()

        pygame.mixer.music.play()

        # Threads for recording and karaoke
        self.recording_thread = threading.Thread(
            target=self.start_recording,
            args=(self.song_length, self.recorded_output_path),
            daemon=True
        )
        self.recording_thread.start()

        self.karaoke_thread = threading.Thread(
            target=self.karaoke_loop,
            daemon=True
        )
        self.karaoke_thread.start()
        self.is_running = True
        self.whiteboard.show_lyrics()

        self.scene_history.append(self.show_play)

    def setup_karaoke_ui(self, selected_item):
        """Set up the UI elements for karaoke."""
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.full_name = selected_item
        if selected_item in self.songs_info and self.songs_info[selected_item] != {}:
            self.full_name = self.songs_info[selected_item]["ar"] + ' - ' + self.songs_info[selected_item]["ti"]
        
        self.lyrics_label = tk.Label(self.frame, font=("Arial", 12), width=80, height=8)
        self.lyrics_label.grid(row=3, column=5, pady=20)

        self.progress_bar = ttk.Progressbar(self.frame, length=500, mode='determinate')
        self.progress_bar.grid(row=6, column=5, pady=20)

        self.countdown_label = tk.Label(self.frame, font=("Arial", 18))
        self.countdown_label.grid(row=8, column=5, pady=20)

        self.restart_button = tk.Button(self.frame, text="Restart", command=self.restart_karaoke)
        self.restart_button.grid(row=1, column=0, pady=10)

        label = tk.Label(self.frame, text=f"Song In play {self.full_name}", font=("Arial", 20))
        label.grid(row=1, column=5, padx=10, pady=10)

        self.stop_button = tk.Button(self.frame, text="Stop", command=self.stop_karaoke)
        self.stop_button.grid(row=1, column=1, pady=10)

        igs.output_set_string("title", f"Now playing {self.full_name}")


    def restart_karaoke(self):
        """Stop current karaoke and restart."""
        self.stop_karaoke()
        self.start_karaoke(self.karaoke_on_play_song)

    def stop_karaoke(self):
        """Stop the karaoke session and clean up."""
        self.karaoke_stop_event.set()
        self.recording_stop_event.set()

        if self.recording_thread:
            self.recording_thread.join(timeout=2)
        if self.karaoke_thread:
            self.karaoke_thread.join(timeout=2)

        pygame.mixer.music.stop()
        self.scene_history.append(self.show_play)
        self.show_play(self.category)

    def start_score_compute(self, record_path):
        """Display content result scene."""
        # Destroy the previous frame if it exists
        if self.frame:
            self.frame.destroy()
        
        # Create a new frame and grid it
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure the row and column to expand
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Create a label to show the result in the main window
        self.result_label = tk.Label(self.frame, text="Result will be shown here.", font=("Arial", 12))
        self.result_label.grid(row=0, column=0, sticky="nsew")

        # Create the loading screen (splash screen)
        self.splash = tk.Toplevel()
        self.splash.title("Loading...")
        self.splash.geometry("300x150")
        
        # Loading label and progress bar
        self.label = tk.Label(self.splash, text="Computing your score, please wait...", font=("Arial", 8))
        self.label.grid(row=0, column=0, padx=20, pady=20)  
       
        # Create a progress bar
        self.progress_bar = ttk.Progressbar(self.splash, orient="horizontal", length=200, mode="indeterminate")
        self.progress_bar.grid(row=1, column=0, padx=20, pady=10)
        
        # Start the loading animation
        self.progress_bar.start(10)

        # Start the long computation in a separate thread
        threading.Thread(target=self.score_computation, args=(record_path,)).start()  

    def score_computation(self, record_path):

        to_compare = os.path.join(self.waves_dir, self.karaoke_on_play_song + '.wav')
        record = os.path.join(self.record_dir, os.path.basename(record_path).split('.')[0] + ".wav")
        result = self.treator.compare_audios(record, to_compare)
        
        player_name = "player_"+ str(uuid.uuid4())
        
        args = (player_name, result, self.full_name, self.level)
        igs.service_call("Tretor", "save_score", args, "")
        
        self.show_result(result)

    def show_result(self, result):
        # Stop the loading screen and show the main app with result
        self.progress_bar.stop()  # Stop the progress animation
        self.splash.destroy()  # Close the loading screen

        done_button = tk.Button(self.frame, text="Main Menu", command=self.show_Menu)
        done_button.grid(row=2, column=5, pady=10)

        replay_button = tk.Button(self.frame, text="Try again !", command=lambda i=self.karaoke_on_play_song: self.start_karaoke(i))
        replay_button.grid(row=2, column=3, pady=10)

        play_an_other_button = tk.Button(self.frame, text="New Game !", command=self.show_select_category)
        play_an_other_button.grid(row=2, column=1, pady=10)

        self.whiteboard.show_score(result) 
        # Show the result in the main app
        self.result_label.config(text=result)
    
    def show_learn_alone(self):
        """Display content for the Learn Alone scene."""
        if self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Title label
        title_label = tk.Label(
            self.frame, text="Learn With the Computer!", font=("Arial", 24)
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))

        # Description label
        description_text = (
            "There will be a succession of sounds that you must first listen to, "
            "then sing them back. The system will evaluate how well you sing and provide a score.\n\n"
            "Three levels of difficulty:\n"
            "  1. Easy: 5 rounds of singing\n"
            "  2. Medium: 12 rounds of singing\n"
            "  3. Hard: 20+ rounds of singing\n\n"
            "Press 'Start' to begin!"
        )

        description_label = tk.Label(self.frame, text=description_text, font=("Arial", 12), justify="left", wraplength=600)
        description_label.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        # Start button
        start_button = tk.Button(self.frame, text="Start", command=self.show_learn_level_choose)
        start_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.whiteboard.init_learn()

        self.scene_history.append(self.show_learn_alone)


    def show_learn_level_choose(self):
        """Display the level selection screen."""
        if self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Level selection buttons
        tk.Label(self.frame, text="Choose a Level", font=("Arial", 20)).grid(row=0, column=0, columnspan=3, pady=(20, 10))

        easy_button = tk.Button(self.frame, text="Easy", command=self.show_learn_easy)
        easy_button.grid(row=1, column=0, padx=20, pady=20)

        medium_button = tk.Button(self.frame, text="Medium", command=self.show_learn_medium)
        medium_button.grid(row=1, column=1, padx=20, pady=20)

        hard_button = tk.Button(self.frame, text="Hard", command=self.show_learn_hard)
        hard_button.grid(row=1, column=2, padx=20, pady=20)

        self.scene_history.append(self.show_learn_level_choose)
        
    def setup_learn_ui(self, level):
        """Set up UI for the learning process."""
        if self.frame:
            self.frame.destroy()
        self.level = level

        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Title
        title_label = tk.Label(self.frame, text=f"Level: {level}", font=("Arial", 20))
        title_label.grid(row=0, column=0, columnspan=3, pady=(20, 10))

        # Lyrics display
        self.lyrics_label = tk.Label(self.frame, font=("Arial", 18), width=60, height=10, wraplength=500, anchor="center")
        self.lyrics_label.grid(row=1, column=0, columnspan=3, pady=20)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.frame, length=500, mode="determinate")
        self.progress_bar.grid(row=2, column=0, columnspan=3, pady=20)

        # Countdown label
        self.countdown_label = tk.Label(self.frame, font=("Arial", 18))
        self.countdown_label.grid(row=3, column=0, columnspan=3, pady=20)

        # Buttons
        restart_button = tk.Button(self.frame, text="Restart", command=self.restart_learn)
        restart_button.grid(row=4, column=0, pady=20)

        stop_button = tk.Button(self.frame, text="Stop", command=self.stop_karaoke)
        stop_button.grid(row=4, column=2, pady=20)

        self.whiteboard.init_learn()

    def restart_learn(self):
        self.stop_karaoke()

        if self.level == 'easy':
            self.show_learn_easy()
        elif self.level == "mid":
            self.show_learn_medium()
        elif self.level == "hard":
            self.show_learn_hard()
        
    def start_learn(self, level, file_name, song):
        """Display content for Karaoke with improved thread and event handling."""

        self.recorded_output_path = os.path.join(self.record_dir, "learn" + level + str(uuid.uuid4()) + ".wav")

        try:
            self.lrc_file_path = os.path.join(self.lrc_dir, file_name + ".lrc")
            self.lyrics_data = self.parse_lrc(self.lrc_file_path)
            pygame.mixer.init()
            pygame.mixer.music.load(song)
            self.song_length = pygame.mixer.Sound(song).get_length()
        except Exception as e:
            print(f"Error loading learn resources: {e}")
            return

        # UI Initialization
        self.setup_learn_ui(level)

        # Countdown before starting
        countdown_time = 5
        for i in range(countdown_time, 0, -1):
            self.countdown_label.config(text=f"Starting in {i}...")
            self.frame.update()
            time.sleep(1)

        self.countdown_label.config(text="Listen Carefully !")
        self.frame.update()
        time.sleep(1)

        pygame.mixer.music.play()
        
        self.karaoke_thread = threading.Thread(
            target=self.karaoke_loop,
            daemon=True
        )
        self.karaoke_thread.start()
        self.is_running = True
        
        self.countdown_label.config(text="Now Sing !")
        self.frame.update()
        
        self.recording_thread = threading.Thread(
            target=self.record_learning,
            args=(song,),
            daemon=True
        )
        self.recording_thread.start()
        self.whiteboard.show_lyrics()
        
        time.sleep(self.song_length)
        
    def record_learning(self, song):
        sample_rate = 48000
        print("Recording...")
        try:
            self.recording = sd.rec(
                int(self.song_length * sample_rate),
                samplerate=sample_rate,
                channels=2,
                dtype='int32'
            )

            # Wait for the recording to finish or stop signal
            elapsed_time = 0
            while elapsed_time < self.song_length:
                time.sleep(0.1)
                elapsed_time += 0.1

            sd.stop()  # Ensure recording stops cleanly

            
            write(self.recorded_output_path, sample_rate, self.recording)
            print(f"Recording saved to {self.recorded_output_path}")
            self.result_learn += self.treator.compare_audios(song, self.recorded_output_path)
                
        except Exception as e:
            print(f"Error during recording: {e}")
        finally:
            self.recording = None
        
    def show_learn_easy(self):
        """Start the Easy level learning session."""
        self.result_learn = 0
        self.level = "easy"

        if self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Randomly select files
        files = [file for file in os.listdir(self.melodies_dir) if os.path.isfile(os.path.join(self.melodies_dir, file))]
        selected_elements = random.sample(files, 5)

        # Process each file
        for file in selected_elements:
            file_name = os.path.splitext(file)[0]
            song_path = os.path.join(self.melodies_dir, file)
            self.start_learn("Easy", file_name, song_path)

        if self.karaoke_thread:
            self.karaoke_thread.join(timeout=2)
        # Show results
        args = ("player" + str(uuid.uuid4()), self.result_learn,'Learn Easy Mode', "Easy")
        igs.service_call("Tretor", "save_score", args, "")
        self.start_score_compute_learn()
        
    def show_learn_medium(self):
        """Start the Medium level learning session."""
        self.result_learn = 0
        self.level = "mid"
        if self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Randomly select files
        files = [file for file in os.listdir(self.melodies_dir) if os.path.isfile(os.path.join(self.melodies_dir, file))]
        selected_elements = random.sample(files, 12)

        # Process each file
        for file in selected_elements:
            file_name = os.path.splitext(file)[0]
            song_path = os.path.join(self.melodies_dir, file)
            self.start_learn("Medium", file_name, song_path)

        # Show results
        args = ("player" + str(uuid.uuid4()), self.result_learn,'Learn Medium Mode', "Medium")
        igs.service_call("Tretor", "save_score", args, "")
        self.start_score_compute_learn()
        
    def show_learn_hard(self):
        """Start the Hard level learning session."""
        self.result_learn = 0
        self.level = "hard"

        if self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Randomly select files
        files = [file for file in os.listdir(self.melodies_dir) if os.path.isfile(os.path.join(self.melodies_dir, file))]

        # Process each file
        for file in files:
            file_name = os.path.splitext(file)[0]
            song_path = os.path.join(self.melodies_dir, file)
            self.start_learn("Hard", file_name, song_path)

        # Show results
        args = ("player" + str(uuid.uuid4()), self.result_learn,'Learn Hard Mode', "Hard")
        igs.service_call("Tretor", "save_score", args, "")
        self.start_score_compute_learn()

    def start_score_compute_learn(self):
        """Display content result scene."""
        # Destroy the previous frame if it exists
        if self.frame:
            self.frame.destroy()
        
        # Create a new frame and grid it
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure the row and column to expand
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Create a label to show the result in the main window
        self.result_label = tk.Label(self.frame, text="Result will be shown here.", font=("Arial", 12))
        self.result_label.grid(row=0, column=0, sticky="nsew")

        # Create the loading screen (splash screen)
        self.splash = tk.Toplevel()
        self.splash.title("Loading...")
        self.splash.geometry("300x150")
        
        # Loading label and progress bar
        self.label = tk.Label(self.splash, text="Computing your score, please wait...", font=("Arial", 8))
        self.label.grid(row=0, column=0, padx=20, pady=20)  
       
        # Create a progress bar
        self.progress_bar = ttk.Progressbar(self.splash, orient="horizontal", length=200, mode="indeterminate")
        self.progress_bar.grid(row=1, column=0, padx=20, pady=10)
        
        # Start the loading animation
        self.progress_bar.start(10)
        
        self.show_result_learn(self.result_learn)   

    def show_result_learn(self, result):
        # Stop the loading screen and show the main app with result
        self.progress_bar.stop()  # Stop the progress animation
        self.splash.destroy()  # Close the loading screen

        done_button = tk.Button(self.frame, text="Main Menu", command=self.show_Menu)
        done_button.grid(row=2, column=5, pady=10)

        replay_button = tk.Button(self.frame, text="Try again !", command=self.show_learn_easy)
        replay_button.grid(row=2, column=3, pady=10)

        play_an_other_button = tk.Button(self.frame, text="New Game !", command=self.show_learn_level_choose)
        play_an_other_button.grid(row=2, column=1, pady=10)

        # Show the result in the main app
        self.whiteboard.show_score(self.result_learn) 
        self.result_label.config(text=result)
        
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
        
        self.load_csv_data("data/others/scores.csv", sort_by)
        
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

