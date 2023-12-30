import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from mutagen.id3 import ID3, ID3NoHeaderError, APIC
from io import BytesIO
import os
import mutagen
import Commands
import Actions
import Settings


class RootApplication:
    genre_table = ["Classique", "Video game Soundtrack", "Film Soundtrack", "Anime Soundtrack",
                   "Song", "Epic Music", "Jazz", "National Anthem"]
    columns_table = ['Nom du fichier', 'Titre', 'Genre', 'Album', 'Date', 'Compositeur', 'Interprète', 'Opus',
                     'Image']
    columns_table_weight = [1, 8, 8, 4, 8, 2, 6, 6, 2, 4, 3]
    technical_names_table = ['title', 'genre', 'album', 'date', 'composer', 'artist', 'tracknumber']
    technical_keys_table = ['TIT2', 'TCON', 'TALB', 'TDRC', 'TCOM', 'TPE1', 'TRCK']
    technical_keys_function_table = [mutagen.id3.TIT2, mutagen.id3.TCON, mutagen.id3.TALB, mutagen.id3.TDRC,
                                     mutagen.id3.TCOM, mutagen.id3.TPE1, mutagen.id3.TRCK]

    def __init__(self):
        # Useful variables
        self.global_fields = {}
        self.row_count = 0
        self.original_image_table = {}
        self.image_table = {}
        self.folder_var = ''

        # Main window
        self.root = tk.Tk()
        self.root.title(Settings.WINDOW_TITLE)
        self.root.geometry(Settings.WINDOW_DEFAULT_SIZE)

        # Menu bar
        self.init_menu_bar()

        # 2 frames of the main window
        self.root.grid_columnconfigure(0, minsize=150)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        tk.Frame(self.root, name='left_frame',
                 bg='red' if Settings.DEBUG_MODE else 'gray27').grid(row=0, column=0, sticky='nsew')
        self.root.nametowidget('left_frame').grid_rowconfigure(11, minsize=120)
        tk.Frame(self.root, name='separator', bg='#FF6000').grid(column=1, row=0, sticky='ns')
        tk.Frame(self.root, name='right_frame', bg='blue' if Settings.DEBUG_MODE else '').grid(row=0, column=2,
                                                                                               sticky='nsew')

        # 2 frames of the table side
        self.root.nametowidget('right_frame').grid_rowconfigure(1, weight=1)
        self.root.nametowidget('right_frame').grid_columnconfigure(0, weight=1)
        tk.Frame(self.root.nametowidget('right_frame'), name='header_frame',
                 bg='green' if Settings.DEBUG_MODE else 'gray27').grid(row=0, column=0, sticky='nsew')
        tk.Frame(self.root.nametowidget('right_frame'), name='table_frame',
                 bg='pink' if Settings.DEBUG_MODE else '').grid(row=1, column=0, sticky='nsew')

        # Create the canvas
        tk.Canvas(self.root.nametowidget('right_frame.table_frame'), name='table_canvas', highlightthickness=0,
                  bg='gray27')
        # Create the scrollbar
        tk.Scrollbar(self.root, orient=tk.VERTICAL, name='main_scrollbar').grid(row=0, column=3, sticky="ns")
        # Config the scrollbar
        self.root.nametowidget('main_scrollbar').config(
            command=self.root.nametowidget('right_frame.table_frame.table_canvas').yview)
        # Bind the scrollbar to the canvas
        self.root.nametowidget('right_frame.table_frame.table_canvas').configure(
            yscrollcommand=self.root.nametowidget('main_scrollbar').set)
        # Pack the canvas
        self.root.nametowidget('right_frame.table_frame.table_canvas').pack(fill=tk.BOTH, expand=True)
        # Create the frame in the canvas
        self.Table = tk.Frame(self.root.nametowidget('right_frame.table_frame.table_canvas'),
                              width=self.root.winfo_screenwidth() - self.root.nametowidget(
                                  'main_scrollbar').winfo_width(),
                              bg='yellow' if Settings.DEBUG_MODE else 'gray27')
        self.Table.pack(fill=tk.BOTH, expand=True)
        # Create the canvas view self
        self.frame_id = self.root.nametowidget('right_frame.table_frame.table_canvas').create_window((0, 0),
                                                                                                     window=self.Table,
                                                                                                     anchor='nw')

        # Bind events on canvas resizing
        self.Table.bind('<Configure>', self.on_configure)
        self.root.nametowidget('right_frame.table_frame.table_canvas').bind('<Configure>', self.on_canvas_configure)
        self.root.nametowidget('right_frame.table_frame.table_canvas').bind_all("<MouseWheel>", self.on_mousewheel)

        # Set Table grid weights
        for index in range(len(self.columns_table_weight)):
            (self.Table.grid_columnconfigure(index, weight=self.columns_table_weight[index], uniform='1'))

        # Table headers
        self.init_table_headers()

        # Left frame buttons
        self.init_left_frame()

        # Create keyboard shortcuts
        self.root.bind("<Control-o>", lambda e: Actions.open_folder(self))
        self.root.bind("<Control-s>", lambda e: self.save_table_to_files())
        self.root.bind("<Configure>", self.on_window_resize)

    def init_menu_bar(self):
        # Create a menu bar
        menubar = tk.Menu(self.root, name="menubar")
        self.root.config(menu=menubar)
        # Create File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Folder", command=lambda: Actions.open_folder(self), accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=lambda: self.save_table_to_files(), accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

    def init_table_headers(self):
        # Set grid weights
        for index in range(len(self.columns_table_weight)):
            (self.root.nametowidget('right_frame.header_frame')
             .grid_columnconfigure(index, weight=self.columns_table_weight[index], uniform='1'))
        # Create the table headers
        for index, head_name in enumerate(self.columns_table):
            ttk.Label(self.root.nametowidget('right_frame.header_frame'), text=self.columns_table[index],
                      relief='solid', name='col' + str(index + 1),
                      anchor='center').grid(column=index + 1, row=0, sticky='ew')

    def init_left_frame(self):
        # Genre field and button
        self.global_fields['genre'] = ttk.Combobox(self.root.nametowidget('left_frame'), values=self.genre_table)
        self.global_fields['genre'].current(0)
        self.global_fields['genre'].grid(column=0, row=0, padx=10, pady=(10, 5), sticky="we")
        tk.Button(self.root.nametowidget('left_frame'), text='Définir le genre global',
                  command=lambda: Commands.set_global_genre(self)).grid(column=0, row=1, padx=10, pady=(5, 10),
                                                                        sticky="we")
        # Album field and button
        self.global_fields['album'] = tk.Text(self.root.nametowidget('left_frame'), height=1, width=10)
        self.global_fields['album'].grid(column=0, row=2, padx=10, pady=(10, 5), sticky="we")
        tk.Button(self.root.nametowidget('left_frame'), text='Définir l\'album global',
                  command=lambda: Commands.set_global_album(self)).grid(column=0, row=3, padx=10, pady=(5, 10),
                                                                        sticky="we")
        # Date field and button
        self.global_fields['date'] = tk.Text(self.root.nametowidget('left_frame'), height=1, width=10)
        self.global_fields['date'].grid(column=0, row=4, padx=10, pady=(10, 5), sticky="we")
        tk.Button(self.root.nametowidget('left_frame'), text='Définir la date globale',
                  command=lambda: Commands.set_global_date(self)).grid(column=0, row=5, padx=10, pady=(5, 10),
                                                                       sticky="we")
        # Composer field and button
        self.global_fields['composer'] = tk.Text(self.root.nametowidget('left_frame'), height=1, width=10)
        self.global_fields['composer'].grid(column=0, row=6, padx=10, pady=(10, 5), sticky="we")
        tk.Button(self.root.nametowidget('left_frame'), text='Définir le compositeur global',
                  command=lambda: Commands.set_global_composer(self)).grid(column=0, row=7, padx=10, pady=(5, 10),
                                                                           sticky="we")
        # Interpret field and button
        self.global_fields['interpret'] = tk.Text(self.root.nametowidget('left_frame'), height=1, width=10)
        self.global_fields['interpret'].grid(column=0, row=8, padx=10, pady=(10, 5), sticky="we")
        tk.Button(self.root.nametowidget('left_frame'), text='Définir l\'interprète global',
                  command=lambda: Commands.set_global_interpret(self)).grid(column=0, row=9, padx=10, pady=(5, 10),
                                                                            sticky="we")
        # Image choosing and setting button
        tk.Button(self.root.nametowidget('left_frame'), text='Définir l\'image globale',
                  command=lambda: Commands.choose_global_image(self)).grid(column=0, row=10, padx=10, pady=10,
                                                                           sticky="ew")
        (tk.Button(self.root.nametowidget('left_frame'), name='set_global_image', text='Appliquer l\'image globale',
                   state=tk.DISABLED, command=lambda: Commands.apply_global_image(self))
         .grid(column=0, row=12, padx=10, pady=10, sticky="ew"))

    # makes frame width match canvas width
    def on_canvas_configure(self, event):
        self.root.nametowidget('right_frame.table_frame.table_canvas').itemconfig(self.frame_id, width=event.width)

    def on_configure(self, _event):
        # update scroll region after starting 'mainloop'
        # when all widgets are in canvas
        self.root.nametowidget('right_frame.table_frame.table_canvas').configure(
            scrollregion=self.root.nametowidget('right_frame.table_frame.table_canvas').bbox('all'))

    def on_window_resize(self, event):
        if event.widget == self.root:
            for i in range(self.row_count):
                if i in self.original_image_table:
                    self.display_row_image(i)
                    self.root.update()

    def on_mousewheel(self, event):
        self.root.nametowidget('right_frame.table_frame.table_canvas').yview_scroll(int(-1 * (event.delta / 120)),
                                                                                    "units")

    def add_file_to_table(self, file, line_index='last'):
        # Default behavior is to append the file to the end of the table
        if line_index == 'last':
            line_index = self.row_count
        # Try to open the file, raise an error if no ID3 tag is found
        try:
            properties = ID3(file)
        except ID3NoHeaderError:
            properties = ID3()
        # Load metadata included in technical_keys_table
        for head_index, head_name in enumerate(self.technical_keys_table):
            (tk.Text(self.Table, height=1, width=1, name='row' + str(line_index) + 'col' + str(head_index + 2))
             .grid(row=line_index, column=head_index + 2, sticky='ew'))
            (self.Table.nametowidget('row' + str(line_index) + 'col' + str(head_index + 2))
             .insert(tk.END, properties.get(head_name) if properties.get(head_name) else ''))
        # Add image container
        (tk.Frame(self.Table, bg='red' if Settings.DEBUG_MODE else '', name='row' + str(line_index) + 'col'
                                                                            + str(len(self.columns_table))).grid(
            row=line_index, column=len(self.columns_table)))
        # Load image
        if properties.get("APIC:"):
            self.add_image_to_row(line_index, BytesIO(properties.get("APIC:").data))
        # Add index
        tk.Text(self.Table, height=1, width=1, name='row' + str(line_index) + 'col0').grid(
            row=line_index, column=0, sticky='ew')
        self.Table.nametowidget('row' + str(line_index) + 'col0').insert(tk.END, str(line_index + 1))
        self.Table.nametowidget('row' + str(line_index) + 'col0').config(state=tk.DISABLED)
        # Add filename
        tk.Text(self.Table, height=1, width=1, name='row' + str(line_index) + 'col1').grid(
            row=line_index, column=1, sticky='ew')
        self.Table.nametowidget('row' + str(line_index) + 'col1').insert(tk.END, os.path.basename(file))
        self.Table.nametowidget('row' + str(line_index) + 'col1').config(state=tk.DISABLED)
        # Add change image button
        (tk.Button(self.Table, text='Editer',
                   command=lambda image_index=line_index: Commands.change_image(self, image_index),
                   name='row' + str(line_index) + 'col' + str(len(self.columns_table) + 1))
         .grid(row=line_index, column=len(self.columns_table) + 1))
        self.root.update()
        self.row_count += 1

    def add_image_to_row(self, line_index, image):
        try:
            self.original_image_table[line_index] = Image.open(image)
            self.display_row_image(line_index)
        except IOError:
            tk.messagebox.showerror('Image non trouvée', 'L\'image sélectionnée n\'a pas pu être ouverte')

    def display_row_image(self, line_index):
        # remove old image if present
        for children in self.Table.nametowidget('row' + str(line_index) + 'col' +
                                                str(len(self.columns_table))).winfo_children():
            children.destroy()
        # get thumbnail width depending on the header width
        thumbnails_width = self.root.nametowidget(
            'right_frame.header_frame.col' + str(self.columns_table.index('Image') + 1)).winfo_width()
        # Transform it to the right size
        thumbnail = (self.original_image_table[line_index]
                     .resize((thumbnails_width, int(self.original_image_table[line_index].height *
                                                    thumbnails_width /
                                                    self.original_image_table[line_index].width)),
                             Image.BILINEAR))
        # Store the image in the object to avoid it getting deleted by the garbage collector
        self.image_table[line_index] = ImageTk.PhotoImage(thumbnail)
        # Add the image to the window
        tk.Label(self.Table.nametowidget('row' + str(line_index) + 'col' + str(len(self.columns_table))),
                 image=self.image_table[line_index]).pack()

    def save_table_to_files(self):
        msg_box = tk.messagebox.askyesno('Sauvegarder les modifications',
                                         'Êtes-vous sûr de vouloir sauvegarder vos modifications ?', icon='warning')
        if msg_box:
            for track_number in range(self.row_count):
                filename = self.Table.nametowidget('row' + str(track_number) + 'col1').get("1.0", "end-1c")
                try:
                    file = ID3()
                    # metadata saving
                    for index, head in enumerate(self.technical_keys_function_table):
                        file.add(head(encoding=3, text=u'' + self.Table.nametowidget(
                            'row' + str(track_number) + 'col' + str(index + 2)).get("1.0", "end-1c").strip() + ''))
                    # Image saving
                    if track_number in self.original_image_table:
                        file.add(APIC(encoding=3, mime='image/jpeg', type=3,
                                      data=Actions.image_to_byte_array(self.original_image_table[track_number])))
                        file.save(self.folder_var + '/' + filename, v2_version=3)
                    # filename saving
                    title = (self.Table.nametowidget('row' + str(track_number) + 'col' +
                                                     str(self.technical_keys_table.index('TIT2') + 2)).get("1.0",
                                                                                                           "end-1c"))
                    if title:
                        if filename != title.strip() + '.mp3':
                            os.rename(self.folder_var + '/' + filename, self.folder_var + '/' + title.strip() + '.mp3')
                            self.Table.nametowidget('row' + str(track_number) + 'col1').config(state=tk.NORMAL)
                            self.Table.nametowidget('row' + str(track_number) + 'col1').delete("1.0", tk.END)
                            self.Table.nametowidget('row' + str(track_number) + 'col1').insert(tk.END,
                                                                                               title.strip() + '.mp3')
                            self.Table.nametowidget('row' + str(track_number) + 'col1').config(state=tk.DISABLED)
                except mutagen.MutagenError:
                    tk.messagebox.showerror('File not found', 'File ' + filename + ' not found')
