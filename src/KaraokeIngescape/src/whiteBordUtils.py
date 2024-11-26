import ingescape as igs
from pathlib import Path
from urllib.parse import urljoin, quote

live_id = None
class WhiteboardUtils:

    def __init__(self):
        self.element_list = {}
        self.live_id = None
        self.current_lyrics = None

    def get_id(self, token):
        return self.element_list.get(token)

    def add_id(self, token, id):
        if token in self.element_list:
            self.element_list[token].append(id)
        else:
            self.element_list[token] = [id]

    def send_message(self, message):
        try:
            igs.service_call("Whiteboard", "chat", message, "")
            # print(f"Message sent: {message}")
        except Exception as e:
            print(f"Failed to send message: {e}")

    def add_Text(self, message, x, y, color, token):
        try:
            arguments_list = (message, x, y, color)
            element_id = igs.service_call("Whiteboard", "addText", arguments_list, token)
            self.add_id(token, element_id)
            return element_id
        except Exception as e:
            print(f"Failed to add text: {e}")
            return None

    def clearWhitboard(self):
        try:
            igs.service_call("Whiteboard", "clear", (), "")
            self.element_list.clear()
        except Exception as e:
            print(f"Failed to clear Whiteboard: {e}")

    def add_image(self, image_url, x, y, width, height, token):
        try:
            img_path = Path(f"data/{image_url}").resolve()
            image_url = f"file:///{img_path}"
            arguments_list = (image_url, x, y, width, height)
            elementID = igs.service_call("Whiteboard", "addImageFromUrl", arguments_list, token)
            self.add_id(token, elementID)
            return elementID
        except Exception as e:
            # print(f"Failed to add image: {e}")
            return None

    def add_Image_From_URL(self, image_name, x, y, token):
        try:
            img_path = Path("data/icones").resolve()
            image_url = urljoin('file:///', quote(str(img_path / image_name)))
            arguments_list = (image_url, x, y)
            elementID = igs.service_call("Whiteboard", "addImageFromUrl", arguments_list, token)
            self.add_id(token, elementID)
            return elementID
        except Exception as e:
            # print(f"Failed to add Image From URL: {e}")
            return None

    def remove_elements(self, token):
        if token in self.element_list:
            for element_id in self.element_list[token]:
                try:
                    igs.service_call("Whiteboard", "remove", (element_id,), "")
                except Exception as e:
                    print(f"Failed to remove element {element_id}: {e}")
            del self.element_list[token]

    def hide_Labels(self, ):
        try:
            igs.service_call("Whiteboard", "hideLabels", (), "")
            # print("Labels hidden")
        except Exception as e:
            print(f"Failed to hide labels: {e}")

    def translate_element(self, elementID, dx, dy):
        try:
            arguments_list = (elementID, dx, dy)
            succeeded = igs.service_call("Whiteboard", "translate", arguments_list, "")
            # print(f"Translated element: {arguments_list}")
            return succeeded
        except Exception as e:
            # print(f"Failed to translate element: {e}")
            return None

    def init_whiteboard_interface(self):
        self.clearWhitboard()
        self.hide_Labels()
        igs.output_set_string("backgroungColor", "gray")
        igs.output_set_string("title", "Ingescape Karaoke App! \n Play Now!")
        self.send_message("Welcome to Ingescape Karaoke!")
        self.send_message("The whiteboard's interface will display all available options.")
        self.send_message("To proceed, select the desired option in the secondary interface.")
        self.add_Image_From_URL("Play.jpg", 50.0, 105.0, "WelcomeInterface")
        self.add_Image_From_URL("Learn.jpg", 425.0, 105.0, "WelcomeInterface")
        self.add_Text("Play", 100.0, 305.0, "Black", "WelcomeInterface")
        self.add_Text("Learn", 475.0, 305.0, "Black", "WelcomeInterface")

    def category_selection_Whiteboard_interface (self): 
    
        self.clearWhitboard()
        self.hide_Labels()

        self.send_message("Select a category of music to display the list of available songs for that category") 
        self.send_message("To proceed you must select the desired option in the secondary interface")
        igs.output_set_string("title", "Choose a music category")

        #add_Image_From_URL("waiting.gif", 225.0, 105.0,"selectCategoryInterface")
        total_width = 800
        total_height = 600
        grid_columns = 2
        grid_rows = 2
        cell_width = total_width / grid_columns
        cell_height = total_height / grid_rows
        gif_width = cell_width * 0.9
        gif_height = cell_height * 0.7

        # Titre de l'interface
        self.add_Text("Let's Play!", total_width / 2 - 50, 10, "Black", "categorySelectionInterface")

        # Positionnement des images et des noms des catégories
        categories = ["Kids", "Commerciale", "Soft", "Rap"]
        image_urls = ["BabySharkDanse.gif", "wakawakaDanse.gif", "someoneLikeYouDanse.gif", "KendrickLamar.gif"] 

        for i in range(4):
            # Calcul des coordonnées
            col = i % grid_columns
            row = i // grid_columns
            x = col * cell_width + (cell_width - gif_width) / 2
            y = row * cell_height + 50  # Laisser un espace pour le texte au-dessus

            # Ajouter le texte de la catégorie
            self.add_Text(categories[i], x + 30, y + 130, "Black", "categorySelectionInterface")

            # Ajouter l'image
            self.add_Image_From_URL(image_urls[i], x, y, "categorySelectionInterface")


    def selection_of_song_Whiteboard_interface(self):
        self.clearWhitboard()
        self.hide_Labels()
        self.send_message("Select the song you would like to sing.")
        self.send_message("To proceed, select an option in the secondary interface.")
        igs.output_set_string("title", "Choose a song")
        self.add_Image_From_URL("waiting.gif", 225.0, 105.0, "selectSongInterface")

    def show_song_preview(self, song_name, song_full_name):
        self.clearWhitboard()
        self.hide_Labels()
        self.send_message("Press 'Play' to listen to the song or 'Stop' to stop.")
        self.send_message("Press 'Start!' to begin karaoke.")
        self.send_message("To proceed, select an option in the secondary interface.")
        igs.output_set_string("title", f"Now playing {song_full_name}")
        self.add_Image_From_URL("KendrickLamar.gif", 225.0, 105.0, "songPreviewInterface")

    def init_karaoke(self, song_full_name):
        self.clearWhitboard()
        self.hide_Labels()

        self.send_message("Sing along!")
        self.send_message("Press 'Restart' to start over or 'Stop' to stop karaoke.")
        self.send_message("To proceed, select an option in the secondary interface.")
        igs.output_set_string("title", f"Now playing {song_full_name}")

    def show_lyrics(self, lrc):
        if self.get_id("lrcs") != None:
            self.remove_elements("lrcs")

        self.add_Text(lrc, 50, 105, "black", "lrcs")

    def show_score(self, score):
        self.clearWhitboard()
        self.hide_Labels()
        text = "Your Score: " + str(score) 
        self.add_Text(text, 330.0, 10.0, "Black", "ScoreInterface")
        self.send_message (text)
        self.add_Image_From_URL("Score2.gif",230.0, 100.00, "ScoreInterface")

    def init_learn(self):
        self.clearWhitboard()
        self.hide_Labels()
        self.send_message("""There will be a succession of sounds that you must first listen to, 
            then sing them back. The system will evaluate how well you sing and provide a score.\n\n
            Three levels of difficulty:\n
            1. Easy: 5 rounds of singing\n
            2. Medium: 12 rounds of singing\n
            3. Hard: 20+ rounds of singing\n\n
            Press 'Start' to begin!""")

        igs.output_set_string("title", f"Learn to sing !")

    def choosed_level(self, level):
        self.send_message(f"Level choosen: {level}")

    def show_learn(self, level):
        self.clearWhitboard()
        self.hide_Labels()
        
        self.send_message("""There will be a succession of sounds that you must first listen to, 
            then sing them back. The system will evaluate how well you sing and provide a score.\n\n
            Three levels of difficulty:\n
            1. Easy: 5 rounds of singing\n
            2. Medium: 12 rounds of singing\n
            3. Hard: 20+ rounds of singing\n\n
            Press 'Start' to begin!""")

        igs.output_set_string("title", f"Learn to sing !")
