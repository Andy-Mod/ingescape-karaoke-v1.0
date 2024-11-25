from KaraokeToolBox import *

if __name__ == "__main__":
    
    treator = Treator()
    
    print("Start comparison")
    print("Comparison score: ", treator.compare_audios("data/wave/euphoria.wav", "data/spleeter/euphoria/euphoria_vocals.wav"))
    