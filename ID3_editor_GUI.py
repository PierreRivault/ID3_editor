import os
import glob

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkintertable import TableCanvas, TableModel


genre_table = ["Classique", "Video game Soundtrack", "Film Soundtrack", "Anime Soundtrack",
               "Song", "Epic Music", "Jazz", "National Anthem"]

columns_table = ['Nom_du_fichier', 'Titre', 'Genre', 'Album', 'Date', 'Compositeur', 'Interprète', 'Opus', 'Image']

folder_var = ""

root = None


def create_table():

    mp3_files = list_mp3_files()

    if not mp3_files:
        tk.messagebox.showinfo("No mp3 file found", "No mp3 file was found in the provided directory")
        return

    tframe = ttk.Frame(root)
    tframe.pack(expand=True, fill=tk.BOTH)

    # Create table columns title
    table = TableCanvas(tframe, rows=0, cols=0)
    table.model.addColumn(columns_table[0])
    table.model.addColumn(columns_table[1])
    table.model.addColumn(columns_table[2])
    table.model.addColumn(columns_table[3])
    table.model.addColumn(columns_table[4])
    table.model.addColumn(columns_table[5])
    table.model.addColumn(columns_table[6])
    table.model.addColumn(columns_table[7])
    table.model.addColumn(columns_table[8])

    table.createTableFrame()


    for file in mp3_files:
        _track = EasyID3(file)
        table.addRow(
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


def main():
    # Create the main window
    global root
    root = tk.Tk()
    root.title("MP3 Renamer")

    # Create a menu bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Create File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Open Folder", command=open_folder)
    file_menu.add_command(label="Save")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=file_menu)

    # Run the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
