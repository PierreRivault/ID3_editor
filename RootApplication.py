import tkinter as tk


class RootApplication:
    genre_table = ["Classique", "Video game Soundtrack", "Film Soundtrack", "Anime Soundtrack",
                   "Song", "Epic Music", "Jazz", "National Anthem"]
    columns_table = ['Nom du fichier', 'Titre', 'Genre', 'Album', 'Date', 'Compositeur', 'Interprète', 'Opus',
                     'Image']
    columns_table_weight = [0, 4, 4, 2, 4, 1, 3, 3, 1, 2, 0]
    technical_names_table = ['title', 'genre', 'album', 'date', 'composer', 'artist', 'tracknumber']

    def __init__(self):
        # Main window
        self.root = tk.Tk()
        # 3 frames of the main window
        self.top_frame = None
        self.middle_frame = None
        self.bottom_frame = None
        # Menu
        self.menu = None
        # Table of all the cells of the grid
        self.table_values = {}
        # Table of the full size images that will be embedded in files when saving
        self.original_image_table = {}
        # Table of the image shown in the window
        self.image_table = {}
        # Folder opened path
        self.folder_var = ""
        # Number of rows in the cell
        self.row_count = 0
        # global text fields
        self.global_genre_field = None
        self.global_album_field = None
        self.global_date_field = None
        self.global_composer_field = None
        self.global_interpret_field = None
        # global image field
        self.global_image_path = None
        # global image shown in the window
        self.global_image = None
