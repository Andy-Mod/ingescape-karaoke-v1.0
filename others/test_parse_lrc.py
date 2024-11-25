from KaraokeToolBox import *

if __name__ == "__main__":
    
    treator = Treator()
    
    print("Start Parsing")
    print("Lrc Parse: ", treator._parse_lrc_file("data/LRCFiles/thehillbillies.lrc", "thehillbillies"))
    