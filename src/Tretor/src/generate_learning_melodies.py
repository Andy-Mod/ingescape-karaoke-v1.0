import os

practice_melodies = [
        {
            "title": "Simple_Scale",
            "notes": ['Do4', 'Re4', 'Mi4', 'Fa4', 'Sol4', 'Fa4', 'Mi4', 'Re4', 'Do4'],
            "durations": [400] * 9,
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 9,
        },
        {
            "title": "Twinkle_Twinkle_Little_Star",
            "notes": ['Do4', 'Do4', 'Sol4', 'Sol4', 'La4', 'La4', 'Sol4', 
                      'Fa4', 'Fa4', 'Mi4', 'Mi4', 'Re4', 'Re4', 'Do4'],
            "durations": [400, 400, 400, 400, 400, 400, 800, 
                          400, 400, 400, 400, 400, 400, 800],
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 14,
        },
        {
            "title": "Arpeggios",
            "notes": ['Do4', 'Mi4', 'Sol4', 'Do5', 'Sol4', 'Mi4', 'Do4', 
                      'Re4', 'Fa4', 'La4', 'Re5', 'La4', 'Fa4', 'Re4'],
            "durations": [300] * 14,
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 14,
        },
        {
            "title": "Chromatic_Challenge",
            "notes": ['Do4', 'Do#4', 'Re4', 'Re#4', 'Mi4', 'Fa4', 'Fa#4', 
                      'Sol4', 'Sol#4', 'La4', 'La#4', 'Si4', 'Do5'],
            "durations": [200] * 13,
            "faddings": [{'fade_in': 30, 'fade_out': 30}] * 13,
        },
        {
            "title": "Large_Intervals",
            "notes": ['Do4', 'Sol4', 'Do5', 'Sol4', 'Mi5', 'Re5', 'Sol4', 'Do5'],
            "durations": [400, 300, 500, 300, 600, 400, 300, 700],
            "faddings": [{'fade_in': 60, 'fade_out': 60}] * 8,
        },
        {
        "title": "Ascending_Steps",
        "notes": ['Do4', 'Re4', 'Mi4', 'Fa4', 'Sol4', 'La4', 'Si4', 'Do5'],
        "durations": [400] * 8,
        "faddings": [{'fade_in': 50, 'fade_out': 50}] * 8,
        },
        {
            "title": "Descending_Steps",
            "notes": ['Do5', 'Si4', 'La4', 'Sol4', 'Fa4', 'Mi4', 'Re4', 'Do4'],
            "durations": [400] * 8,
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 8,
        },
        {
            "title": "Scale_Up_and_Down",
            "notes": ['Do4', 'Re4', 'Mi4', 'Fa4', 'Sol4', 'Fa4', 'Mi4', 'Re4', 'Do4'],
            "durations": [300] * 9,
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 9,
        },
        {
            "title": "Pentatonic_Scale",
            "notes": ['Do4', 'Re4', 'Mi4', 'Sol4', 'La4', 'Sol4', 'Mi4', 'Re4', 'Do4'],
            "durations": [400] * 9,
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 9,
        },
        {
            "title": "Triad_Practice",
            "notes": ['Do4', 'Mi4', 'Sol4', 'Do5', 'Sol4', 'Mi4', 'Do4'],
            "durations": [500] * 7,
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 7,
        },
        {
            "title": "Minor_Arpeggios",
            "notes": ['Do4', 'Mib4', 'Sol4', 'Do5', 'Sol4', 'Mib4', 'Do4'],
            "durations": [500] * 7,
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 7,
        },
        {
            "title": "Jumping_Fifths",
            "notes": ['Do4', 'Sol4', 'Re4', 'La4', 'Mi4', 'Si4', 'Fa4', 'Do5'],
            "durations": [400] * 8,
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 8,
        },
        {
            "title": "Interval_Expansion",
            "notes": ['Do4', 'Re4', 'Mi4', 'Fa4', 'Sol4', 'La4', 'Si4', 'Do5', 'Mi5', 'Sol5'],
            "durations": [300, 300, 300, 400, 400, 500, 500, 600, 600, 700],
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 10,
        },
        {
            "title": "Octave_Jumps",
            "notes": ['Do4', 'Do5', 'Re4', 'Re5', 'Mi4', 'Mi5', 'Fa4', 'Fa5'],
            "durations": [600, 600, 600, 600, 600, 600, 600, 600],
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 8,
        },
        {
            "title": "Chromatic_Steps",
            "notes": ['Do4', 'Do#4', 'Re4', 'Re#4', 'Mi4', 'Fa4', 'Fa#4', 'Sol4'],
            "durations": [200] * 8,
            "faddings": [{'fade_in': 30, 'fade_out': 30}] * 8,
        },
        {
            "title": "Diatonic_Jumps",
            "notes": ['Do4', 'Mi4', 'Sol4', 'Do5', 'Re5', 'Fa5', 'La5', 'Si5', 'Do6'],
            "durations": [400] * 9,
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 9,
        },
        {
            "title": "Syncopated_Rhythms",
            "notes": ['Do4', 'Re4', 'Mi4', 'Fa4', 'Sol4', 'Fa4', 'Mi4', 'Re4', 'Do4'],
            "durations": [400, 300, 500, 300, 400, 300, 500, 300, 800],
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 9,
        },
        {
            "title": "Complex_Syncopation",
            "notes": ['Do4', 'Sol4', 'La4', 'Do5', 'Sol4', 'Mi4', 'Fa4', 'Re4'],
            "durations": [500, 300, 500, 300, 500, 300, 600, 700],
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 8,
        },
        {
            "title": "Swing_Feel",
            "notes": ['Do4', 'Re4', 'Mi4', 'Fa4', 'Sol4', 'Fa4', 'Mi4', 'Re4', 'Do4'],
            "durations": [300, 600, 300, 600, 300, 600, 300, 600, 800],
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 9,
        },
        {
            "title": "Ascending_Chromatics",
            "notes": ['Do4', 'Do#4', 'Re4', 'Re#4', 'Mi4', 'Fa4', 'Fa#4', 'Sol4', 'Sol#4'],
            "durations": [300] * 9,
            "faddings": [{'fade_in': 30, 'fade_out': 30}] * 9,
        },
        {
            "title": "Descending_Chromatics",
            "notes": ['Sol4', 'Fa#4', 'Fa4', 'Mi4', 'Re#4', 'Re4', 'Do#4', 'Do4'],
            "durations": [300] * 8,
            "faddings": [{'fade_in': 30, 'fade_out': 30}] * 8,
        },
        {
            "title": "Dynamic_Intervals",
            "notes": ['Do4', 'Sol4', 'Do5', 'Re5', 'Fa4', 'La4', 'Si4', 'Do5'],
            "durations": [400, 500, 400, 600, 300, 500, 400, 700],
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 8,
        },
        {
            "title": "Mixed_Rhythms",
            "notes": ['Do4', 'Re4', 'Mi4', 'Fa4', 'Sol4', 'La4', 'Si4', 'Do5'],
            "durations": [200, 400, 300, 600, 200, 700, 400, 500],
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 8,
        },
        {
            "title": "Fast_Chromatic_Run",
            "notes": ['Do4', 'Do#4', 'Re4', 'Re#4', 'Mi4', 'Fa4', 'Fa#4', 'Sol4', 'Sol#4', 'La4', 'La#4', 'Si4', 'Do5'],
            "durations": [200] * 13,
            "faddings": [{'fade_in': 30, 'fade_out': 30}] * 13,
        },
        {
            "title": "Unpredictable_Jumps",
            "notes": ['Do4', 'Sol4', 'Re4', 'La4', 'Mi5', 'Fa4', 'Do5', 'Re5'],
            "durations": [500, 300, 600, 400, 700, 500, 300, 800],
            "faddings": [{'fade_in': 50, 'fade_out': 50}] * 8,
        }
    ]
    

def generate_practice_melodies_with_lyrics(practice_meolodies, treator):

    lyrics_content = []
    tmp = []
    
    for melody in practice_meolodies:
        notes, durations, faddings, name = melody['notes'], melody['durations'], melody['faddings'], melody['title'].lower()
        
        lyrics_metadata = [
        f"[id: {name}]",
        "[ar: KaraokeToolBox]",
        "[al: Practice Melodies]",
        f"[ti: {name}]"
        ]
        
        treator._generate_melodie(notes, durations, faddings, name, save=True)
        
        current_time = 0
        for note, duration in zip(notes, durations):
            minutes = int(current_time // 60000)
            seconds = (current_time % 60000) / 1000
            time_stamp = f"[{minutes:02}:{seconds:05.2f}]"
            tmp.append(f"{time_stamp}{note}")
            current_time += duration
            
        lyrics_metadata.append(f"[length: {current_time}]")    
        lyrics_content.extend(lyrics_metadata)
        
        lyrics_content.extend(tmp)
        
        # Save lyrics content
        lyrics_text = "\n".join(lyrics_content)
        
        lyrics_file_path = os.path.join("data", "LRCFiles", f"{name}.lrc")
        os.makedirs(os.path.dirname(lyrics_file_path), exist_ok=True)
        with open(lyrics_file_path, "w") as file:
            file.write(lyrics_text)
        
        lyrics_content, tmp = [], []
