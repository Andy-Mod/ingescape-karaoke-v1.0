#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Tretor.py
#  Tretor
#  Created by Ingenuity i/o on 2024/11/15
#
# <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
# <html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
# p, li { white-space: pre-wrap; }
# hr { height: 1px; border-width: 0; }
# li.unchecked::marker { content: "\2610"; }
# li.checked::marker { content: "\2612"; }
# </style></head><body style=" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;">
# <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">T<span style=" font-size:13px; color:#2a2a2a;">ool box for background computation and treatments for the karaoke app </span></p></body></html>
#
import ingescape as igs
from KaraokeToolBox import *
import os
import json

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Tretor(metaclass=Singleton):
    def __init__(self):
        # outputs
        self._outputO = None
        
        # atributes
        current_file = os.path.abspath(__file__)
        dir = current_file.replace(os.path.basename(current_file), "")
        root_dir = os.path.join(dir, "../../../")
        os.chdir(root_dir)
        print(root_dir, os.getcwd())

        self._treator = Treatment() 

    # outputs
    @property
    def outputO(self):
        return self._outputO

    @outputO.setter
    def outputO(self, value):
        self._outputO = value
        if self._outputO is not None:
            igs.output_set_string("output", self._outputO)
    @property
    def tretorO(self):
        return self._tretorO

    @tretorO.setter
    def tretorO(self, value):
        self._tretorO = value
        if self._tretorO is not None:
            igs.output_set_data("tretor", value)

    def _set_tretor(self, value):
        self._tretorO = value

    # services
    def run_pretreatment(self, sender_agent_name, sender_agent_uuid):
        print("start service: run_pretreatment")
        self._treator.run_pretreatment()

    def save_melodie(self, sender_agent_name, sender_agent_uuid, output_file):
        print("start service: save_melodie")
        self._treator._save_melodie(output_file)

    def play_melodie(self, sender_agent_name, sender_agent_uuid, melodie):
        print("start service: play_melodie")
        melody = AudioSegment.from_wav(melodie) 
        self._treator._play_melodie(melody)

    def generate_melodie(self, sender_agent_name, sender_agent_uuid, informations):
        print("start service: generate_melodie")
        infos = json.load(informations)
        print(f"Playing: {infos['title']}")

        self._treator._generate_melodie(
            infos['notes'],
            infos['durations'],
            infos['faddings'],
            infos['title'].lower()
        )

        outpath = os.path.join("data/melodies/", informations['title'].lower() + '.wav')

        return os.path.abspath(outpath)

    def merge_audios(self, sender_agent_name, sender_agent_uuid, audio_1_path, audio_2_path):
        print("start service: merge_audios")
        name = os.path.basename(audio_1_path)[0] + "+" + os.path.basename(audio_2_path)[0]
        outpath = os.path.join("data/record", name + ".wav")
        self._treator._merge_audios(audio_1_path, audio_2_path, output_file=outpath)

        return os.path.abspath(outpath)

    def save_file_informations(self, sender_agent_name, sender_agent_uuid, path_to_json_file):
        print("start service: save_file_informations")
        self._treator._save_file_informations(path_to_json_file)

    def load_song_infos(self, sender_agent_name, sender_agent_uuid, path_to_json_file):
        print("start service: load_song_infos")
        dict = self._treator._load_song_infos(path_to_json_file)

        return json.dumps(dict, indent=4)

    def save_score(self, sender_agent_name, sender_agent_uuid, player_id, score, song_name, level):
        print("start service: save_score")
        self._treator._save_score(player_id, score, song_name, level)

    def compare_audios(self, sender_agent_name, sender_agent_uuid, audio_file_1, audio_file_2):
        print("start service: compare_audios")
        return self._treator.compare_audios(audio_file_1, audio_file_2)

    def extract_features(self, sender_agent_name, sender_agent_uuid, input_file, output_dir="data/audio_features"):
        print("start service: extract_features")
        file_name = os.path.basename(input).split('.')[0]
        feature_file = os.path.join(output_dir, file_name + "_features.json")

        self._treator._extract_features(input_file)

        return feature_file

    def separate_audio(self, sender_agent_name, sender_agent_uuid, input_file, output_dir="data/spleeter/"):
        print("start service: separate_audio")
        return self._treator._separate_audio(input_file)


    def transcribe(self, sender_agent_name, sender_agent_uuid, input_file, output_dir="data/lyrics/"):
        print("start service: transcribe")
        return self._treator._transcribe(input_file)

    def  parse_lrc_file(self, sender_agent_name, sender_agent_uuid, file_name, path_to_lrc):
        print("start service: parse_lrc_file")
        return self._treator._parse_lrc_file(path_to_lrc, file_name)

    def convert_to_wav(self, sender_agent_name, sender_agent_uuid, input_file, output_dir="data/wave/"):
        print("start service: convert_to_wav")
        return self._treator._convert_to_wav(input_file)

    def get_frequency(self, sender_agent_name, sender_agent_uuid, note, octave):
        print("start service: get_frequency")
        return self._treator._get_frequency(note, octave)


