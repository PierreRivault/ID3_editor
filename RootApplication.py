import tkinter as tk
from PIL import ImageTk, Image


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
        # Canvas of the second frame
        self.canvas = None
        self.frame_id = None
        # Frame inside the canvas
        self.canvas_frame = None
        # Scrollbar for the canvas frame
        self.scrollbar = None
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

    # makes frame width match canvas width
    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.frame_id, width=event.width)

    def on_configure(self, event):
        # update scroll region after starting 'mainloop'
        # when all widgets are in canvas
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def on_window_resize(self, event):
        if event.widget == self.root:
            for i in range(self.row_count):
                if i in self.original_image_table:
                    thumbnail = (self.original_image_table[i].resize((self.table_values[0]['Image'].winfo_width(),
                                 int(self.original_image_table[i].height * self.table_values[0][
                                     'Image'].winfo_width() / self.original_image_table[i].width)),
                                 Image.BILINEAR))
                    self.image_table[i] = ImageTk.PhotoImage(thumbnail)
                    # Remove old image from the GUI
                    for children in self.table_values[i + 1]['image_container'].winfo_children():
                        children.destroy()
                    self.table_values[i + 1]['Image'] = tk.Label(self.table_values[i + 1]['image_container'],
                                                                 image=self.image_table[i])
                    self.table_values[i + 1]['Image'].pack()
                    self.table_values[i + 1].update()
            self.root.update()
            self.root.update_idletasks()
