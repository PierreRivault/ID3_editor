import tkinter as tk
from tkintertable import TableModel


class RootApplication:
    genre_table = ["Classique", "Video game Soundtrack", "Film Soundtrack", "Anime Soundtrack",
                   "Song", "Epic Music", "Jazz", "National Anthem"]
    columns_table = ['Nom du fichier', 'Titre', 'Genre', 'Album', 'Date', 'Compositeur', 'Interprète', 'Opus',
                     'Image']
    columns_table_weight = [2, 1, 4, 4, 2, 4, 1, 3, 3, 1, 2, 2]
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
        self.table_values = {}
