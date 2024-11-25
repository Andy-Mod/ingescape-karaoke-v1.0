import tkinter as tk
import pyaudio
import wave
import simpleaudio as sa
import threading

class AudioRecorderPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder and Player")
        self.root.geometry("400x300")

        self.is_recording = False
        self.is_playing = False
        self.frames = []
        self.recording_thread = None
        self.playback_object = None

        
        self.setup_ui()

    def setup_ui(self):
        
        self.record_button = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.record_button.pack(pady=10)

        self.stop_record_button = tk.Button(self.root, text="Stop Recording", state=tk.DISABLED, command=self.stop_recording)
        self.stop_record_button.pack(pady=10)
        
        self.play_button = tk.Button(self.root, text="Play Audio", command=self.play_audio, state=tk.DISABLED)
        self.play_button.pack(pady=10)

        self.stop_play_button = tk.Button(self.root, text="Stop Audio", command=self.stop_audio, state=tk.DISABLED)
        self.stop_play_button.pack(pady=10)

        
        self.status_label = tk.Label(self.root, text="Status: Ready")
        self.status_label.pack(pady=20)

    def start_recording(self):
        """Start recording audio."""
        self.is_recording = True
        self.frames = []
        self.record_button.config(state=tk.DISABLED)
        self.stop_record_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Recording...")

        self.recording_thread = threading.Thread(target=self.record)
        self.recording_thread.start()

    def record(self):
        """Record audio using PyAudio."""
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 44100
        chunk = 1024
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

        while self.is_recording:
            data = self.stream.read(chunk)
            self.frames.append(data)

    def stop_recording(self):
        """Stop recording audio."""
        self.is_recording = False
        self.recording_thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        with wave.open("data/recorded.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))

        self.record_button.config(state=tk.NORMAL)
        self.stop_record_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Recording Stopped. File Saved.")

    def play_audio(self):
        """Play the recorded audio file."""
        self.play_button.config(state=tk.DISABLED)
        self.stop_play_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Playing Audio...")
        
        self.playing_thread = threading.Thread(target=self.play_audio_file)
        self.playing_thread.start()

    def play_audio_file(self):
        """Use simpleaudio to play the audio file."""
        with wave.open("data/recorded.wav", "rb") as wf:
            audio_data = wf.readframes(wf.getnframes())
            self.playback_object = sa.play_buffer(audio_data, wf.getnchannels(), wf.getsampwidth(), wf.getframerate())
            self.playback_object.wait_done()
        
        self.stop_play_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Ready")

    def stop_audio(self):
        """Stop the playback of the audio file."""
        if self.playback_object is not None:
            self.playback_object.stop()
        self.stop_play_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Playback Stopped")


root = tk.Tk()
app = AudioRecorderPlayerApp(root)
root.mainloop()
