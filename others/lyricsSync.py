import re
import time
import pygame
import tkinter as tk
from tkinter import ttk
import threading

class KaraokeApp:
    def __init__(self, lrc_file_path, song_file_path):
        self.lrc_file_path = lrc_file_path
        self.song_file_path = song_file_path
        self.lyrics_data = self.parse_lrc(lrc_file_path)
        self.current_lyric_index = 0
        pygame.mixer.init()
        pygame.mixer.music.load(song_file_path)
        
        self.root = tk.Tk()
        self.root.title("Karaoke App")
        self.root.geometry("600x400")

        self.lyrics_label = tk.Label(self.root, font=("Arial", 24), width=40, height=5)
        self.lyrics_label.pack(pady=50)

        self.progress_bar = ttk.Progressbar(self.root, length=500, mode='determinate')
        self.progress_bar.pack(pady=20)

        self.countdown_label = tk.Label(self.root, font=("Arial", 18))
        self.countdown_label.pack(pady=20)

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
        except FileNotFoundError:
            print(f"Error: The file '{lrc_file_path}' was not found.")
        except Exception as e:
            print(f"Error: {e}")
        
        return lyrics_data

    def update_lyrics_display(self):
        current_time = pygame.mixer.music.get_pos() / 1000
        while self.current_lyric_index < len(self.lyrics_data) and self.lyrics_data[self.current_lyric_index]['timestamp'] <= current_time:
            self.lyrics_label.config(text=self.lyrics_data[self.current_lyric_index]['lyric'])
            self.current_lyric_index += 1

        song_length = pygame.mixer.Sound(self.song_file_path).get_length()
        progress = current_time / song_length * 100
        self.progress_bar['value'] = progress

    def karaoke_loop(self):
        while pygame.mixer.music.get_busy():
            self.update_lyrics_display()
            self.root.update_idletasks()
            self.root.update()
            time.sleep(0.01)

    def start_karaoke(self):
        countdown_time = 5
        for i in range(countdown_time, 0, -1):
            self.countdown_label.config(text=f"Starting in {i}...")
            self.root.update()
            time.sleep(1)
        
        self.countdown_label.config(text="Let's Sing!")
        self.root.update()
        time.sleep(1)
        
        pygame.mixer.music.play()
        
        karaoke_thread = threading.Thread(target=self.karaoke_loop)
        karaoke_thread.daemon = True
        karaoke_thread.start()
        
        self.root.mainloop()
        
        self.root.quit()  # Close the app after the song finishes

if __name__ == "__main__":
    lrc_file_path = 'data/LRCFiles/twinkle_twinkle.lrc'
    song_file_path = 'data/melodies/twinkle_twinkle_little_star.wav'
    
    karaoke_app = KaraokeApp(lrc_file_path, song_file_path)
    karaoke_app.start_karaoke()
