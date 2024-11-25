from KaraokeToolBox import Treatment

if __name__ == "__main__":
    
    treator = Treatment()
    
    print("Start comparison")
    print("Comparison score: ", treator.compare_audios("data/wave/euphoria.wav", "data/wave/thehillbillies.wav"))
    