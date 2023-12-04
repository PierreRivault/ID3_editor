import os
import glob

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, BOTTOM
from tkintertable import TableCanvas, TableModel


genre_table = ["Classique", "Video game Soundtrack", "Film Soundtrack", "Anime Soundtrack",
               "Song", "Epic Music", "Jazz", "National Anthem"]

columns_table = ['Nom_du_fichier', 'Titre', 'Genre', 'Album', 'Date', 'Compositeur', 'Interprète', 'Opus', 'Image']
technical_names_table = ['title', 'genre', 'album', 'date', 'composer', 'performer', 'tracknumber']

folder_var = ""

root = None

model = TableModel()

table = None


def create_table():
    global model
    global table

    mp3_files = list_mp3_files()

    if not mp3_files:
        tk.messagebox.showinfo("No mp3 file found", "No mp3 file was found in the provided directory")
        return

    tframe = ttk.Frame(root)
    tframe.pack(expand=True, fill="both")

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
    for track_number in range(model.getRowCount()):
        filename = model.getRecName(track_number)
        track = model.getRecordAtRow(track_number)
        file = EasyID3(folder_var+'/'+filename)
        for i in range(len(columns_table)):
            if i == 0 or i == len(columns_table)-1:
                continue
            print(technical_names_table[i-1], ':', track[columns_table[i]].strip())
            file[technical_names_table[i-1]] = track[columns_table[i]].strip()
            if technical_names_table[i-1] == 'performer':
                file['artist'] = track[columns_table[i]].strip()
        file.save()
        if track['Titre']:
            os.rename(folder_var+'/'+filename, folder_var+'/'+track['Titre'].strip()+".mp3")
            model.setRecName(track['Titre'], track_number)
            model.data[track_number][columns_table[0]] = track['Titre'].strip()+".mp3"
            table.redraw()

    return


def main():
    # Create the main window
    global root
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

    save_button = tk.Button(root, text="Sauvegarder", command=save_metadata)
    save_button.pack(side=BOTTOM)

    root.bind("<Control-o>", lambda e: open_folder())
    root.bind("<Control-s>", lambda e: save_metadata())

    # Run the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
