from Whiteboard_services import *



def launch_whiteborad_interface( elementID_list):
    clearWhitboard()
    hide_Labels()
    send_message("Welcome to Ingescape Karaoke") 
    add_Text ( "Welcome to Ingescape Karaoke", 150.0,10.0, "Blue", "WelcomInterface")
    add_Image_From_URL("Learn.jpg", 50.0, 105.0,"WelcomInterface")
    add_Image_From_URL("Play.jpg", 300.0, 105.0,"WelcomInterface")
    add_Text("Learn", 100.0, 305.0,"Black","WelcomInterface")
    add_Text("Play", 350.0, 305.0,"Black","WelcomInterface")
    send_message("You must click on the Python interface button if you want to learn to sing or play karoke")    

def category_selection_Whiteboard_interface (elementID_list): 
    # Whiteboard Interface
    clearWhitboard()
    hide_Labels()
    send_message("You need to click on the button in the Python interface of the category you want to sing.") 
    # Définir les paramètres de l'interface
    total_width = 800
    total_height = 600
    grid_columns = 2
    grid_rows = 2
    cell_width = total_width / grid_columns
    cell_height = total_height / grid_rows
    gif_width = cell_width * 0.9
    gif_height = cell_height * 0.7

    # Titre de l'interface
    add_Text("Let's Play!", total_width / 2 - 50, 10, "Black", "categorySelectionInterface")

    # Positionnement des images et des noms des catégories
    categories = ["Kids", "Commerciale", "Soft", "Rap"]
    image_urls = ["BabySharkDance.gif", "WakaWakaDance.gif", "someoneLikeYou.gif", "KendrickLamar.gif"] 

    for i in range(4):
        # Calcul des coordonnées
        col = i % grid_columns
        row = i // grid_columns
        x = col * cell_width + (cell_width - gif_width) / 2
        y = row * cell_height + 50  # Laisser un espace pour le texte au-dessus

        # Ajouter le texte de la catégorie
        add_Text(categories[i], x + 30, y + 130, "Black", "categorySelectionInterface")

        # Ajouter l'image
        add_image(image_urls[i], x, y, gif_width, gif_height, "categorySelectionInterface")

def music_selection_whiteboard_interface(elementID_list, categorie, selected_categories_url, selected_categories_names):
    # Clear the whiteboard interface to start fresh
    clearWhitboard()
    # Display a message to the user
    send_message("You need to click on the button in the Python interface of the music you want to sing.")
    
    # Define the dimensions of the interface
    total_width = 800  # Total width of the whiteboard interface
    total_height = 600  # Total height of the whiteboard interface
    grid_columns = 2  # Number of columns in the grid
    grid_rows = 2  # Number of rows in the grid
    cell_width = total_width / grid_columns +100 # Width of each grid cell
    cell_height = total_height / grid_rows  # Height of each grid cell
    gif_width = cell_width * 0.9  # Width of the image or GIF within each cell
    gif_height = cell_height * 0.7  # Height of the image or GIF within each cell

    # Add the title to the interface
    add_Text("Let's Play!", total_width / 2 - 50, 10, "Black", "MusicSelectionInterface")
    
    # Loop through the first 4 music options to add their text and images
    for i in range(4):
        # Calculate the coordinates for the current grid cell
        col = i % grid_columns  # Determine the column index
        row = i // grid_columns  # Determine the row index
        x = col * cell_width + (cell_width - gif_width) / 2 + 10  # X-coordinate of the image
        y = row * cell_height + 30  # Y-coordinate of the image (with space for text above)

        # Add the music name text to the interface
        add_Text(selected_categories_names[i], x + 30, y + 150, "Black", "MusicSelectionInterface")

        # Add the image for the music
        add_image(selected_categories_url[i], x, y, gif_width, gif_height, "MusicSelectionInterface")

def playing_whiteboard_interface():
    pass
def testing_music_whiteboard_interface(music):
    pass
def score_whiteboard_interface(score):
    pass
def learn_categroy_whiteboard_ineterface ():
    pass
def learning_whiteboard_interface():
    pass

