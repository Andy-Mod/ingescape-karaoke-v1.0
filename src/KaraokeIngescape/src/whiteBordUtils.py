import ingescape as igs
import os
from pathlib import Path
from urllib.parse import urljoin, quote

live_id = None
# Fonction pour envoyer un message au Whiteboard
def send_message(message):
    try:
        igs.service_call("Whiteboard", "chat", message, "")
        print(f"Message sent: {message}")
    except Exception as e:
        print(f"Failed to send message: {e}")


def add_Text(message,  x, y, color, token):
    try:
        arguments_list = (message,x,y,color)
        elementID = igs.service_call("Whiteboard", "addText", arguments_list, token)
        print(f"add Test: {arguments_list}")
        return elementID 
    except Exception as e:
        print(f"Failed to add Text: {e}")

def add_image(image_url, x, y, width, height, token):
        """Ajoute une image sur le tableau blanc."""
        img_path =f"C:/Users/ghazo/Documents/Ingescape/sandbox/KaraokeIngescape/data/{image_url}"
        image_url = f"file:///{img_path}"
        arguments_list = (image_url, x, y, width, height)
        elementID = igs.service_call("Whiteboard", "addImageFromUrl", arguments_list, token)
        igs.service_call("Whiteboard", "addImageFromUrl", (image_url, x, y, width, height), token)

def add_Image_From_URL(image_name, x, y, token):
    try:
        # Define the image path
        img_path = Path("data/icones").resolve()
        # Build the full image URL
        image_url = urljoin('file:///', quote(str(img_path / image_name)))
        # Prepare arguments for the service call
        arguments_list = (image_url, x, y)
        # Make the service call
        elementID = igs.service_call("Whiteboard", "addImageFromUrl", arguments_list, token)
        print(f"Added Image From URL: {arguments_list}")
        return elementID
    except Exception as e:
        print(f"Failed to add Image From URL: {e}")


def remove_Element (elemntID):
    try: 
        succeeded = igs.service_call("Whiteboard", "remove", elemntID, "")
        print(f"remove: {elemntID}")
        return succeeded
    except Exception as e:
        print(f"Failed to remove: {e}")

def hide_Labels ():
    try:
        igs.service_call("Whiteboard", "hideLabels",(),"")
        print("hide Labels")
    except Exception as e:
        print(f"Failed to hide labels: {e}")

def translate_element(elementId, dx, dy):
    try:
        arguments_list = (elementId, dx, dy)
        succ = igs.service_call("Whiteboard", "translate", arguments_list, "")
        print(f"translate: {arguments_list}")
        return succ 
    except Exception as e:
        print(f"Failed to add Text: {e}")

def clearWhitboard():
    try:
        igs.service_call("Whiteboard", "clear",(),"")
    except Exception as e:
        print(f"Failed to clear: {e}")

def init_whiteboard_interface():
    clearWhitboard()
    hide_Labels()

    igs.output_set_string("backgroungColor", "gray")
    igs.output_set_string("title", "Ingescape Karaoke App ! \n Play Now !")

    send_message("Welcome to Ingescape Karaoke !") 
    send_message("The whiteboard's interface will deplay all of the available options")
    send_message("To proceed you must select the desired option in the secondary interface") 

    add_Image_From_URL("Play.jpg", 50.0, 105.0,"WelcomInterface")
    add_Image_From_URL("Learn.jpg", 425.0, 105.0,"WelcomInterface")
    add_Text("Play", 100.0, 305.0,"Black","WelcomInterface")
    add_Text("Learn", 475.0, 305.0,"Black","WelcomInterface")

def category_selection_Whiteboard_interface (): 
    
    clearWhitboard()
    hide_Labels()

    send_message("Select a category of music to display the list of available songs for that category") 
    send_message("To proceed you must select the desired option in the secondary interface")
    igs.output_set_string("title", "Choose a music category")

    add_Image_From_URL("waiting.gif", 225.0, 105.0,"selectCategoryInterface")

def selection_of_song_Whiteboard_interface(): 
    
    clearWhitboard()
    hide_Labels()

    send_message("Select the song you would like to sing") 
    send_message("To proceed you must select the desired option in the secondary interface")
    igs.output_set_string("title", "Choose a song")

    add_Image_From_URL("waiting.gif", 225.0, 105.0,"selectSongInterface")

def show_song_preview(song_name, song_full_name): 
    
    clearWhitboard()
    hide_Labels()

    send_message("""Press the button "Play" to listen to the song, the button "Stop" to stop.""") 
    send_message("""To start the karaoke, press the button "Start !" """) 
    send_message("To proceed you must select the desired option in the secondary interface")
    igs.output_set_string("title", f"Now playing {song_full_name}")

    add_Image_From_URL("KendrickLamar.gif", 225.0, 105.0,"songPreviewInterface")

def init_karaoke(song_full_name):
    clearWhitboard()
    hide_Labels()

    send_message("Go ahead and sing !") 
    send_message("""Press the button "Restart" to start over and the button "Stop" to stop the ongoing karaoke. """)
    send_message("To proceed you must select the desired option in the secondary interface")
    igs.output_set_string("title", f"Now playing")

def show_lyrics(lrcs, song_full_name):
    remove_Element(live_id)

    live_id = add_Text(lrcs, 50, 105.5,"Black", "lrcs")
    igs.output_set_string("title", f"Now playing")
