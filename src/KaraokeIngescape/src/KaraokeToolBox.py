import numpy as np # numpy==1.25
from pydub import AudioSegment
from pydub.playback import play
from pydub.generators import Sine
from spleeter.separator import Separator
import whisper
import librosa
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import logging
import warnings
import tensorflow as tf
import csv

# Suppress verbose logging and set GPU usage off
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings
logging.getLogger('spleeter').setLevel(logging.ERROR)
logging.getLogger('whisper').setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

class Treatment:
    def __init__(self, data_path='data/mp3/', whisper_model_path='base', score_path="data/others/scores.csv"):
        self.data_path = data_path
        self.score_path = score_path
        self.transcriber = whisper.load_model(whisper_model_path)
        self.separator = Separator('spleeter:2stems')
        
        self._note_frequencies = {
            'Do': {1: 32.70, 2: 65.41, 3: 130.81, 4: 261.63, 5: 523.25, 6: 1046.50, 7: 2093.00, 8: 4186.01},
            'Do#': {1: 34.65, 2: 69.30, 3: 138.59, 4: 277.18, 5: 554.37, 6: 1108.73, 7: 2217.46, 8: 4434.92},
            'Reb': {1: 34.65, 2: 69.30, 3: 138.59, 4: 277.18, 5: 554.37, 6: 1108.73, 7: 2217.46, 8: 4434.92},
            'Re': {1: 36.71, 2: 73.42, 3: 146.83, 4: 293.66, 5: 587.33, 6: 1174.66, 7: 2349.32, 8: 4698.64},
            'Re#': {1: 38.89, 2: 77.78, 3: 155.56, 4: 311.13, 5: 622.25, 6: 1244.51, 7: 2489.02, 8: 4978.03},
            'Mib': {1: 38.89, 2: 77.78, 3: 155.56, 4: 311.13, 5: 622.25, 6: 1244.51, 7: 2489.02, 8: 4978.03},
            'Mi': {1: 41.20, 2: 82.41, 3: 164.81, 4: 329.63, 5: 659.26, 6: 1318.51, 7: 2637.02, 8: 5274.04},
            'Fa': {1: 43.65, 2: 87.31, 3: 174.61, 4: 349.23, 5: 698.46, 6: 1396.91, 7: 2793.83, 8: 5587.65},
            'Fa#': {1: 46.25, 2: 92.50, 3: 185.00, 4: 369.99, 5: 739.99, 6: 1479.98, 7: 2959.96, 8: 5919.91},
            'Solb': {1: 46.25, 2: 92.50, 3: 185.00, 4: 369.99, 5: 739.99, 6: 1479.98, 7: 2959.96, 8: 5919.91},
            'Sol': {1: 49.00, 2: 98.00, 3: 196.00, 4: 392.00, 5: 783.99, 6: 1567.98, 7: 3135.96, 8: 6271.93},
            'Sol#': {1: 51.91, 2: 103.83, 3: 207.65, 4: 415.30, 5: 830.61, 6: 1661.22, 7: 3322.44, 8: 6644.88},
            'Lab': {1: 51.91, 2: 103.83, 3: 207.65, 4: 415.30, 5: 830.61, 6: 1661.22, 7: 3322.44, 8: 6644.88},
            'La': {1: 55.00, 2: 110.00, 3: 220.00, 4: 440.00, 5: 880.00, 6: 1760.00, 7: 3520.00, 8: 7040.00},
            'La#': {1: 58.27, 2: 116.54, 3: 233.08, 4: 466.16, 5: 932.33, 6: 1864.66, 7: 3729.31, 8: 7458.62},
            'Sib': {1: 58.27, 2: 116.54, 3: 233.08, 4: 466.16, 5: 932.33, 6: 1864.66, 7: 3729.31, 8: 7458.62},
            'Si': {1: 61.74, 2: 123.47, 3: 246.94, 4: 493.88, 5: 987.77, 6: 1975.53, 7: 3951.07, 8: 7902.13}
        }

        current_file = os.path.abspath(__file__)
        dir = current_file.replace(os.path.basename(current_file), "")
        root_dir = os.path.join(dir, "../")
        os.chdir(root_dir)
        print(root_dir, os.getcwd())
    
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
    
    def _get_frequency(self, note, octave):
        return self._note_frequencies.get(note, {}).get(octave, None)

    def _convert_to_wav(self, input_file, output_dir="data/wave/"):
        os.makedirs(output_dir, exist_ok=True)
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, file_name + ".wav")
        
        if not os.path.exists(output_file):
            audio = AudioSegment.from_file(input_file)
            audio.export(output_file, format="wav")
            print(f"Converted {input_file} to WAV format.")
        return output_file
    def _parse_lrc_file(self, path_to_lrc, file_name):
        out_path = os.path.join("data", "lyrics", file_name + ".txt")
        lrc = ""
        with open(path_to_lrc, "r") as file:
            for row in file:
                tmp = row.split(":")[0]
                if tmp[1:].isdigit():
                    lrc += " "
                    lrc += row.split(']')[-1][:-1]
        
        with open(out_path, "w") as file:
            file.write(lrc)
        print(file_name, lrc)

        return lrc 

    def _transcribe(self, input_file, output_dir="data/lyrics/"):
        os.makedirs(output_dir, exist_ok=True)
        file_name = input_file.split('/')[-1].split('.')[0].split('_')[0]
        output_file = os.path.join(output_dir, file_name + ".txt")
        lrc_path = os.path.join("data", "LRCFiles", file_name + ".lrc")

        if os.path.exists(output_file):
            with open(output_file, "r") as file:
                return file.read()
        
        if os.path.exists(lrc_path):    
            out = self._parse_lrc_file(lrc_path, file_name)
            with open(output_file, "w") as file:
                file.write(out)
        
        result = self.transcriber.transcribe(input_file)["text"]
        
        with open(output_file, "w") as file:
            file.write(result)
            print(f"Saved transcription for {input_file}.")
        
        return result

    def _separate_audio(self, input_file, output_dir="data/spleeter/"):
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        init_vocals_path = os.path.join(output_dir, file_name, "vocals.wav")
        init_accompaniment_path = os.path.join(output_dir, file_name, "accompaniment.wav")
        
        renamed_vocals_path = os.path.join(output_dir, file_name, file_name + "_vocals.wav")
        renamed_accompaniment_path = os.path.join(output_dir, file_name, file_name + "_accompaniment.wav")

        if os.path.exists(renamed_vocals_path) and os.path.exists(renamed_accompaniment_path):
            print(f"Separation already exists for {input_file}.")

        self.separator.separate_to_file(input_file, output_dir)
        os.rename(init_vocals_path, renamed_vocals_path)
        os.rename(init_accompaniment_path, renamed_accompaniment_path)
        print(f"Separated vocals and accompaniment for {input_file}.")
        
        return renamed_vocals_path, renamed_accompaniment_path

    def _extract_features(self, audio_file, output_dir="data/audio_features"):
        file_name = os.path.basename(audio_file).split('.')[0]
        feature_file = os.path.join(output_dir, file_name + "_features.json")
        

        if os.path.exists(feature_file):
            print(f"Loading cached features for {audio_file}")
            with open(feature_file, "r") as file:
                return json.load(file)
        text = self._transcribe(audio_file)
        
        y, sr = librosa.load(audio_file)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_track = [np.max(pitches[i]) for i in range(pitches.shape[0]) if np.max(pitches[i]) > 0]
        average_pitch = np.mean(pitch_track) if pitch_track else 0
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        duration = librosa.get_duration(y=y, sr=sr)    
        text = self._transcribe(audio_file)
        if isinstance(tempo, np.ndarray):
            tempo = float(tempo[0])

        norm = float(np.linalg.norm(np.array(pitch_track)))
        output = {
            "bpm": tempo,
            "duration": duration,
            "average_pitch": float(average_pitch),
            "pitch_track": norm,
            "text": text,
            "pitch_range": len(pitch_track)
        }
        
        output = {key: value.tolist() if isinstance(value, np.ndarray) else value for key, value in output.items()}
        
        os.makedirs(output_dir, exist_ok=True)
        with open(feature_file, "w") as file:
            json.dump(output, file, indent=4)

        return output
    
    def _calculate_text_similarity(self, text1, text2):
        return abs(text1.__hash__() - text1.__hash__())

    def compare_audios(self, file1, file2):
        """Compare two audio files based on their pitch, tempo, length, and text similarity."""
        
        feature1 = self._extract_features(file1)
        feature2 = self._extract_features(file2)

        pk, pq = feature1["pitch_range"], feature2["pitch_range"]

        length_difference_threshold = 0.5  
        if feature1["duration"] * length_difference_threshold - feature2["duration"] > 0 or feature2["duration"] * length_difference_threshold - feature1["duration"] > 0  :
            return 0.0 
        
        pitch_diff = np.abs(feature1["pitch_track"] - feature2["pitch_track"])
        tempo_diff = abs(feature1["bpm"] - feature2["bpm"])
        
        text_similarity = 0.0  
        if feature1["text"] and feature2["text"]:  
            text_similarity = self._calculate_text_similarity(feature1["text"], feature2["text"])

        pitch_range = max([pk, pq])
        tempo_range = max([feature1["bpm"], feature2["bpm"]])  

        normalized_tempo_diff = tempo_diff / tempo_range
        normalized_pitch_diff = pitch_diff / pitch_range
        
        print(text_similarity)
        print(normalized_pitch_diff + normalized_tempo_diff)

        score = (1 - normalized_pitch_diff - normalized_tempo_diff)*0.15 + (1 - text_similarity)*0.85
        
        return max(score, 0) * 15000
    
    def _save_score(self, player, score, song_name, level):
        data = []
        with open(self.score_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)

        data.append([player, song_name, level, score])

        with open(self.score_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        print("score saved")

    def _load_song_infos(self, path_json_file):
        if os.path.exists(path_json_file):
            print(f"Loading existing songs informations from  {path_json_file}")
            with open(path_json_file, "r") as file:
                return json.load(file)
        else:
            print("Fichier inexistant") 
            return {}


    def _save_file_informations(self, path_json_file):
        tmp_dic = {}
        if os.path.exists(path_json_file):
            print(f"Loading existing songs informations from  {path_json_file}")
            with open(path_json_file, "r") as file:
                songs_info =  json.load(file)
        else :
            with open(path_json_file, "w") as file:
                pass
            
        files = [file for file in os.listdir("data/LRCFiles") if os.path.isfile(os.path.join("data/LRCFiles", file))]
        for file in files:
            file_name = file.split('.')[0]
            if file_name not in songs_info:
                path_to_lrc = os.path.join("data", "LRCFiles", file)
                
                with open(path_to_lrc, "r") as LRC_file:
                    for row in LRC_file:
                        tmp = row.split(":")
                        key = tmp[0][1:]
                        if not key.isdigit() and key != "length":
                            tmp_dic[key] = tmp[-1].split("]")[0]
                        else:
                            break
                    print(tmp_dic)
                if tmp_dic != {}:
                    songs_info[file_name] = tmp_dic
                tmp_dic = {}
        with open(path_json_file, "w") as file:
            json.dump(songs_info, file, indent=4)
    
    def _merge_audios(self, audio_file_1, audio_file_2, output_file="merged_audio.wav"):
        audio1 = AudioSegment.from_wav(audio_file_1)  
        audio2 = AudioSegment.from_wav(audio_file_2)  

        if audio1.frame_rate != audio2.frame_rate:
            raise ValueError("Sample rates do not match! Resampling is required.")
        if audio1.channels != audio2.channels:
            raise ValueError("Number of channels (mono/stereo) do not match!")

        if len(audio1) > len(audio2):
            audio2 = audio2 + AudioSegment.silent(duration=len(audio1) - len(audio2))
        elif len(audio2) > len(audio1):
            audio1 = audio1 + AudioSegment.silent(duration=len(audio2) - len(audio1))

        merged_audio = audio1.overlay(audio2)

        merged_audio.export("merged_audio.wav", format="wav")

        print("Audio files merged successfully!")

    def _generate_melodie(self, notes, durations, faddings, name = "generated", save=True):
        melody = AudioSegment.silent(duration=0)

        for note, duration, fadding in zip(notes, durations, faddings):
            note_name, octave = note[:-1], int(note[-1])  
            frequency = self._get_frequency(note_name, octave)
            
            if frequency is not None:
                
                note_audio = Sine(frequency).to_audio_segment(duration=duration)
                
                fade_in_duration = fadding.get('fade_in', 0)
                fade_out_duration = fadding.get('fade_out', 0)
                note_audio = note_audio.fade_in(fade_in_duration).fade_out(fade_out_duration)
                    
                melody += note_audio
            else:
                print(f"Invalid note: {note}")
                break
        
        if save:
            self._save_melodie(melody, "data/melodies/"+ name + '.wav')                    
        return melody
    
    def _generate_melodie_with_metronome(self, notes, durations, faddings, name="generated", save=True, metronome_bpm=120):
        from pydub.generators import Sine  # Ensure we use a tone generator for the metronome
        
        melody = AudioSegment.silent(duration=0)
        metronome_click = Sine(1000).to_audio_segment(duration=50).fade_out(20)  # High-pitched click

        # Calculate the metronome interval in milliseconds
        metronome_interval = 60000 / metronome_bpm
        total_duration = sum(durations)

        # Generate the full metronome track
        metronome_track = AudioSegment.silent(duration=total_duration)
        metronome_position = 0
        while metronome_position < total_duration:
            metronome_track = metronome_track.overlay(metronome_click, position=metronome_position)
            metronome_position += metronome_interval

        # Generate the melody
        current_position = 0
        for note, duration, fadding in zip(notes, durations, faddings):
            note_name, octave = note[:-1], int(note[-1])  
            frequency = self._get_frequency(note_name, octave)
            
            if frequency is not None:
                # Create the note sound
                note_audio = Sine(frequency).to_audio_segment(duration=duration)
                fade_in_duration = fadding.get('fade_in', 0)
                fade_out_duration = fadding.get('fade_out', 0)
                note_audio = note_audio.fade_in(fade_in_duration).fade_out(fade_out_duration)
                
                # Add the note to the melody
                melody += note_audio
            else:
                print(f"Invalid note: {note}")
                break
        
        # Combine melody and metronome
        combined_track = melody.overlay(metronome_track)

        # Optionally save the generated melody
        if save:
            self._save_melodie(combined_track, "data/melodies/" + name + '.wav')

        return combined_track

    
    def _play_melodie(self, melody):
        play(melody)
    
    def _save_melodie(self, melody, output_file="generated_melody.wav"):
        melody.export(output_file, format="wav")
        print(f"Melody saved as {output_file}")


    def run_pretreatment(self):
        # generate melodies for learning mode with lirycs 

        files = self.list_files_by_subdirectory("data/mp3")
        
        for sub_dir in files:
            for file in files[sub_dir]:
                print(sub_dir, file)
                full_path = os.path.join(self.data_path, sub_dir, file)
                print(f"Processing file: {file}")
                
                wav_file = self._convert_to_wav(full_path)
                vocals, _ = self._separate_audio(wav_file)
                self._transcribe(vocals)

                self._save_file_informations("data/others/songs_info.json")
            
        print("Pre-treatment process completed successfully.")


if __name__ == "__main__":
    
    treator = Treatment()
    treator.run_pretreatment()
    
    print("Start comparison")
    print("Comparison score: ", treator.compare_audios("data/mp3/i.mp3", "data/recorded.wav"))
