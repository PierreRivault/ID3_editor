import tkinter as tk
from tkintertable import TableModel


class RootApplication:
    genre_table = ["Classique", "Video game Soundtrack", "Film Soundtrack", "Anime Soundtrack",
                   "Song", "Epic Music", "Jazz", "National Anthem"]
    columns_table = ['Nom_du_fichier', 'Titre', 'Genre', 'Album', 'Date', 'Compositeur', 'Interprète', 'Opus',
                     'Image']
    technical_names_table = ['title', 'genre', 'album', 'date', 'composer', 'artist', 'tracknumber']

    def __init__(self):
        self.folder_var = ""
        self.model = TableModel()
        self.root = tk.Tk()
        self.table = None
        self.top_frame = None
        self.middle_frame = None
        self.bottom_frame = None
        self.menu = None
        self.global_genre_field = None
        self.global_album_field = None
        self.global_date_field = None
        self.global_composer_field = None
        self.global_interpret_field = None
        self.global_image_path = None
        self.global_image = None
