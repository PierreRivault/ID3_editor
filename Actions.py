import Commands

import glob
import os
from mutagen.easyid3 import EasyID3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkintertable import TableCanvas

from mutagen.id3 import ID3, APIC


def init_window(window):
    window.root.title("MP3 Editor")
    window.root.geometry('480x270')

    # Create a menu bar
    menubar = tk.Menu(window.root)
    window.root.config(menu=menubar)

    # Create File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Open Folder", command=lambda: open_folder(window), accelerator="Ctrl+O")
    file_menu.add_command(label="Save", command=lambda: save_metadata(window), accelerator="Ctrl+S")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=window.root.destroy)
    menubar.add_cascade(label="File", menu=file_menu)

    # Adjust the weights of the main window grid to fill the space
    window.root.grid_rowconfigure(1, weight=1)
    window.root.grid_columnconfigure(0, weight=1)

    # Create the first frame
    top_frame = tk.Frame(window.root)
    top_frame.grid(row=0, column=0, sticky='nsew')

    # Create the second frame
    middle_frame = tk.Frame(window.root)
    middle_frame.grid(row=1, column=0, sticky='nsew')

    # Create the third frame
    bottom_frame = tk.Frame(window.root)
    bottom_frame.grid(row=2, column=0, sticky='nsew')

    # Create elements of the first frame, global values
    top_frame.grid_columnconfigure(0, weight=1)
    top_frame.grid_columnconfigure(7, weight=1)
    # Genre field and button
    window.global_genre_field = ttk.Combobox(top_frame, values=window.genre_table)
    window.global_genre_field.current(0)
    window.global_genre_field.grid(column=1, row=0, padx=10, pady=10, sticky="we")
    global_genre_button = tk.Button(top_frame, text='Définir le genre global',
                                    command=lambda: Commands.set_global_genre(window))
    global_genre_button.grid(column=1, row=1, padx=10, pady=10)
    # Album field and button
    window.global_album_field = tk.Text(top_frame, height=1, width=10)
    window.global_album_field.grid(column=2, row=0, padx=10, pady=10, sticky="we")
    global_album_button = tk.Button(top_frame, text='Définir l\'album global',
                                    command=lambda: Commands.set_global_album(window))
    global_album_button.grid(column=2, row=1, padx=10, pady=10)
    # Date field and button
    window.global_date_field = tk.Text(top_frame, height=1, width=10)
    window.global_date_field.grid(column=3, row=0, padx=10, pady=10, sticky="we")
    global_date_button = tk.Button(top_frame, text='Définir la date globale',
                                   command=lambda: Commands.set_global_date(window))
    global_date_button.grid(column=3, row=1, padx=10, pady=10)
    # Composer field and button
    window.global_composer_field = tk.Text(top_frame, height=1, width=10)
    window.global_composer_field.grid(column=4, row=0, padx=10, pady=10, sticky="we")
    global_composer_button = tk.Button(top_frame, text='Définir le compositeur global',
                                       command=lambda: Commands.set_global_composer(window))
    global_composer_button.grid(column=4, row=1, padx=10, pady=10)
    # Interpret field and button
    window.global_interpret_field = tk.Text(top_frame, height=1, width=10)
    window.global_interpret_field.grid(column=5, row=0, padx=10, pady=10, sticky="we")
    global_interpret_button = tk.Button(top_frame, text='Définir l\'interprète global',
                                        command=lambda: Commands.set_global_interpret(window))
    global_interpret_button.grid(column=5, row=1, padx=10, pady=10)
    # Image choosing and setting button
    global_image_choosing_button = tk.Button(top_frame, text='Définir l\'image globale',
                                             command=lambda: Commands.choose_global_image(window))
    global_image_choosing_button.grid(column=6, row=0, padx=10, pady=10)
    global_image_setting_button = tk.Button(top_frame, text='Définir le  global',
                                            command=lambda: Commands.set_global_image(window))
    global_image_setting_button.grid(column=6, row=1, padx=10, pady=10)

    # Create elements of the second frame
    # Create the table canvas
    window.table = TableCanvas(middle_frame, window.model, rows=0, cols=0)
    window.table.maxcellwidth = 600
    window.table.autoresizecols = True
    # Create the columns
    for i in range(len(window.columns_table)):
        window.table.model.addColumn(window.columns_table[i])

    # Create elements of the third frame, commands
    save_button = tk.Button(bottom_frame, text="Sauvegarder", command=lambda: save_metadata(window))
    save_button.pack()

    # Create keyboard shortcuts
    window.root.bind("<Control-o>", lambda e: open_folder(window))
    window.root.bind("<Control-s>", lambda e: save_metadata(window))

    return window


def list_mp3_files(folder_var):
    fpath = u"%s/*.mp3" % folder_var
    files = glob.glob(fpath)
    return files


def create_table(window):

    # table.adjustColumnWidths()
    window.table.show()

    # List mp3 files in the folder
    mp3_files = list_mp3_files(window.folder_var)

    if not mp3_files:
        tk.messagebox.showinfo("No mp3 file found", "No mp3 file was found in the provided directory")
        return

    for file in mp3_files:
        _track = EasyID3(file)

        window.table.addRow(
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



def open_folder(window):
    folder_path = filedialog.askdirectory()
    if folder_path:
        window.folder_var = folder_path
        create_table(window)  # Call create_table after setting folder_var


def save_metadata(window):
    msg_box = tk.messagebox.askyesno('Sauvegarder les modifications',
                                     'Êtes-vous sûr de vouloir sauvegarder vos modifications ?', icon='warning')
    if msg_box:
        for track_number in range(window.model.getRowCount()):
            filename = window.model.getRecName(track_number)
            track = window.model.getRecordAtRow(track_number)
            file = EasyID3(window.folder_var + '/' + filename)
            for i in range(len(window.columns_table)):
                if i == 0 or i == len(window.columns_table) - 1:
                    continue
                file[window.technical_names_table[i - 1]] = track[window.columns_table[i]].strip()
                if window.technical_names_table[i - 1] == 'performer':
                    file['artist'] = track[window.columns_table[i]].strip()
            file.save()
            if track['Titre']:
                if window.model.getRecName(track_number).strip() != track['Titre'].strip() + '.mp3':
                    os.rename(window.folder_var + '/' + filename,
                              window.folder_var + '/' + track['Titre'].strip() + ".mp3")
                    window.model.setRecName(track['Titre'].strip() + '.mp3', track_number)
                    window.model.data[track['Titre'].strip() + '.mp3'][window.columns_table[0]] = track[
                                                                                                      'Titre'].strip() + '.mp3'
                    window.table.redrawTable()

    return
