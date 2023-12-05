import os
import glob

import commands

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, BOTTOM, BOTH
from tkintertable import TableCanvas, TableModel

genre_table = ["Classique", "Video game Soundtrack", "Film Soundtrack", "Anime Soundtrack",
               "Song", "Epic Music", "Jazz", "National Anthem"]

columns_table = ['Nom_du_fichier', 'Titre', 'Genre', 'Album', 'Date', 'Compositeur', 'Interprète', 'Opus', 'Image']
technical_names_table = ['title', 'genre', 'album', 'date', 'composer', 'performer', 'tracknumber']

folder_var = ""

model = TableModel()

global table


def create_table():
    global model
    global table

    mp3_files = list_mp3_files()

    if not mp3_files:
        tk.messagebox.showinfo("No mp3 file found", "No mp3 file was found in the provided directory")
        return

    tframe = ttk.Frame(middle_frame)
    tframe.pack(expand=True, fill=BOTH)

    # Create table columns title
    table = TableCanvas(tframe, model, rows=0, cols=0)
    for i in range(len(columns_table)):
        table.model.addColumn(columns_table[i])

    table.createTableFrame()

    for file in mp3_files:
        _track = EasyID3(file)

        table.addRow(
            key=os.path.basename(file),
            Nom_du_fichier=os.path.basename(file),
            Titre=_track['title'][0] if 'title' in _track else '',
            Genre=_track['genre'][0] if 'genre' in _track else '',
            Album=_track['album'][0] if 'album' in _track else '',
            Date=_track['date'][0] if 'date' in _track else '',
            Compositeur=_track['composer'][0] if 'composer' in _track else '',
            Interprète=_track['performer'][0] if 'performer' in _track else '',
            Opus=_track['tracknumber'][0] if 'tracknumber' in _track else '',
            Image=''
        )

    table.adjustColumnWidths()
    table.show()


def open_folder():
    global folder_var
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_var = folder_path
        create_table()  # Call create_table after setting folder_var


def list_mp3_files():
    fpath = u"%s/*.mp3" % folder_var
    files = glob.glob(fpath)
    return files


def save_metadata():
    global model
    msg_box = tk.messagebox.askquestion('Sauvegarder les modifications',
                                        'Êtes-vous sûr de vouloir sauvegarder vos modifications ?', icon='warning')
    if msg_box:
        for track_number in range(model.getRowCount()):
            filename = model.getRecName(track_number)
            track = model.getRecordAtRow(track_number)
            file = EasyID3(folder_var + '/' + filename)
            for i in range(len(columns_table)):
                if i == 0 or i == len(columns_table) - 1:
                    continue
                file[technical_names_table[i - 1]] = track[columns_table[i]].strip()
                if technical_names_table[i - 1] == 'performer':
                    file['artist'] = track[columns_table[i]].strip()
            file.save()
            if track['Titre']:
                if model.getRecName(track_number).strip() != track['Titre'].strip() + '.mp3':
                    os.rename(folder_var + '/' + filename, folder_var + '/' + track['Titre'].strip() + ".mp3")
                    model.setRecName(track['Titre'].strip() + '.mp3', track_number)
                    model.data[track['Titre'].strip() + '.mp3'][columns_table[0]] = track['Titre'].strip() + '.mp3'
                    table.redrawTable()

    return


# Create the main window
root = tk.Tk()
root.title("MP3 Editor")
root.geometry('480x270')

# Create a menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Create File menu
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Open Folder", command=open_folder, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_metadata, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=file_menu)

# Adjust the weights of the main window grid to fill the space
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create the first frame
top_frame = tk.Frame(root)
top_frame.grid(row=0, column=0, sticky='nsew')

# Create the second frame
middle_frame = tk.Frame(root)
middle_frame.grid(row=1, column=0, sticky='nsew')

# Create the third frame
bottom_frame = tk.Frame(root)
bottom_frame.grid(row=2, column=0, sticky='nsew')

# Create elements of the first frame, global values
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(7, weight=1)
# Genre field and button
global_genre_field = tk.Text(top_frame, height=1, width=10)
global_genre_field.grid(column=1, row=0, padx=10, pady=10, sticky="we")
global_genre_button = tk.Button(top_frame, text='Définir le genre global', command=commands.set_global_genre)
global_genre_button.grid(column=1, row=1, padx=10, pady=10)
# Album field and button
global_album_field = tk.Text(top_frame, height=1, width=10)
global_album_field.grid(column=2, row=0, padx=10, pady=10, sticky="we")
global_album_button = tk.Button(top_frame, text='Définir l\'album global', command=commands.set_global_album)
global_album_button.grid(column=2, row=1, padx=10, pady=10)
# Date field and button
global_date_field = tk.Text(top_frame, height=1, width=10)
global_date_field.grid(column=3, row=0, padx=10, pady=10, sticky="we")
global_date_button = tk.Button(top_frame, text='Définir la date globale', command=commands.set_global_date)
global_date_button.grid(column=3, row=1, padx=10, pady=10)
# Composer field and button
global_composer_field = tk.Text(top_frame, height=1, width=10)
global_composer_field.grid(column=4, row=0, padx=10, pady=10, sticky="we")
global_composer_button = tk.Button(top_frame, text='Définir le compositeur global', command=commands.set_global_composer)
global_composer_button.grid(column=4, row=1, padx=10, pady=10)
# Interpret field and button
global_interpret_field = tk.Text(top_frame, height=1, width=10)
global_interpret_field.grid(column=5, row=0, padx=10, pady=10, sticky="we")
global_interpret_button = tk.Button(top_frame, text='Définir l\'interprète global', command=commands.set_global_interpret)
global_interpret_button.grid(column=5, row=1, padx=10, pady=10)
# Image choosing and setting button
global_image_choosing_button = tk.Button(top_frame, text='Définir l\'image globale', command=commands.choose_global_image)
global_image_choosing_button.grid(column=6, row=0, padx=10, pady=10)
global_image_setting_button = tk.Button(top_frame, text='Définir le  global', command=commands.set_global_image)
global_image_setting_button.grid(column=6, row=1, padx=10, pady=10)

# Create elements of the third frame, commands
save_button = tk.Button(bottom_frame, text="Sauvegarder", command=save_metadata)
save_button.pack()

# Create keyboard shortcuts
root.bind("<Control-o>", lambda e: open_folder())
root.bind("<Control-s>", lambda e: save_metadata())

# Run the Tkinter event loop
root.mainloop()
