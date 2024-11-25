import tkinter as tk
from tkinter import ttk
from KaraokeIngescape import *
from Whiteboard_services import *

from WhiteboardInterface import * 


# Fonction pour afficher la nouvelle interface
def music_selection_interface(root, elementID_list, categorie):

 
    image_urls_Kids = ["BabyShark", "file", "file", "file"] 
    image_urls_commerciale = ["BabyShark", "file", "file", "file"] 
    image_urls_Soft  = ["Boheme.jpg", "lovely.jpg", "voila.jpg", "SomeoneLikeYou.jpg"] 
    image_urls_rap = ["BabyShark", "file", "file", "file"] 

    music_names_Soft = ["Boheme", "Lovely", "Voila", "Someone Like You"] 
    music_names_Kids = ["Boheme", "Lovely", "Voila", "Someone Like You"] 
    music_names_Commerciale = ["Boheme", "Lovely", "Voila", "Someone Like You"] 
    music_names_rap = ["Boheme", "Lovely", "Voila", "Someone Like You"] 
    categories = {"kids": [image_urls_Kids,music_names_Kids], "commerciale":[image_urls_commerciale,music_names_Commerciale], "Soft":[image_urls_Soft,music_names_Soft] , "rap":[image_urls_rap,music_names_rap]}
    selected_categories_url = categories[categorie][0]
    selected_categories_names = categories[categorie][1]

    music_selection_whiteboard_interface (elementID_list, categorie, selected_categories_url,selected_categories_names)
 
    # Suppression des widgets de la première interface
    for widget in root.winfo_children():
        widget.destroy()

    # Titre de la nouvelle interface
    new_title = tk.Label(
        root,
        text="Let's Play!",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#2d2f30"
    )
    new_title.pack(pady=20)

    # Cadre pour les boutons en 2 lignes * 2 colonnes
    new_button_frame = tk.Frame(root, bg="#2d2f30")
    new_button_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    # Création des boutons en 2x2
    id=0
    for i in range(2):
        for j in range(2):
            new_button = ttk.Button(
                new_button_frame,
                text=selected_categories_names[id],
                command=lambda text=selected_categories_names[id]: print(f"{text} clicked"),
                style="New.TButton"
            )
            new_button.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")  # "nsew" permet d'étirer le bouton
            id+=1
    # Configuration pour que les lignes et colonnes s'adaptent
    for i in range(3):
        new_button_frame.grid_rowconfigure(i, weight=1)  # Pour que chaque ligne ait le même poids
    for j in range(2):
        new_button_frame.grid_columnconfigure(j, weight=1)  # Pour que chaque colonne ait le même poids


# Fonction pour afficher la nouvelle interface
def category_selection_interface(root, elementID_list):
    #Whiteboard interface
    category_selection_Whiteboard_interface(elementID_list)

    categories = ["kids", "commerciale", "Soft", "rap"]
    # Suppression des widgets de la première interface
    for widget in root.winfo_children():
        widget.destroy()

    # Titre de la nouvelle interface
    new_title = tk.Label(
        root,
        text="Let's Play!",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#2d2f30"
    )
    new_title.pack(pady=20)

    # Cadre pour les boutons en 2 lignes * 2 colonnes
    new_button_frame = tk.Frame(root, bg="#2d2f30")
    new_button_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    # Création des boutons en 2x2
    id=0
    for i in range(2):
        for j in range(2):
            new_button = ttk.Button(
                new_button_frame,
                text=categories[id],
                command= lambda category=categories[id]: music_selection_interface(root, elementID_list, category),
                style="New.TButton"
            )
            new_button.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")  # "nsew" permet d'étirer le bouton
            id+=1
    # Configuration pour que les lignes et colonnes s'adaptent
    for i in range(3):
        new_button_frame.grid_rowconfigure(i, weight=1)  # Pour que chaque ligne ait le même poids
    for j in range(2):
        new_button_frame.grid_columnconfigure(j, weight=1)  # Pour que chaque colonne ait le même poids




# Création de la fenêtre principale
def launch_interface(elementID_list):

    launch_whiteborad_interface(elementID_list)

    #Pyhton Interface
    root = tk.Tk()
    root.title("Ingescape Karaoke")
    root.configure(bg="#2d2f30")

    # Titre
    title_label = tk.Label(
        root,
        text="Welcome to Ingescape Karaoke",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#2d2f30"
    )
    title_label.pack(pady=20)

    # Cadre pour les boutons
    button_frame = tk.Frame(root, bg="#2d2f30")
    button_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    # Bouton Learn
    learn_button = ttk.Button(
        button_frame,
        text="Learn",
        command=lambda: print("Learn clicked"),
        style="Learn.TButton"
    )
    learn_button.grid(row=0, column=0, padx=20, sticky="nsew")

    # Bouton Play
    play_button = ttk.Button(
        button_frame,
        text="Play",
        command=lambda: category_selection_interface(root, elementID_list),
        style="Play.TButton"
    )
    play_button.grid(row=0, column=1, padx=20, sticky="nsew")

    # Styles pour les boutons
    style = ttk.Style()
    style.configure("Learn.TButton", font=("Arial", 12), background="#4CAF50", foreground="black")
    style.configure("Play.TButton", font=("Arial", 12), background="#FF5722", foreground="black")

    # Configuration pour que les lignes et colonnes s'adaptent
    button_frame.grid_rowconfigure(0, weight=1)  # Pour que la première ligne ait le même poids
    button_frame.grid_columnconfigure(0, weight=1)  # Pour que la première colonne ait le même poids
    button_frame.grid_columnconfigure(1, weight=1)  # Pour que la deuxième colonne ait le même poids

    root.mainloop()

