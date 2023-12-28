import io

import mutagen
import Commands
import glob
import os
from io import BytesIO
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image

from mutagen.id3 import ID3, APIC


def list_mp3_files(folder_var):
    fpath = u"%s/*.mp3" % folder_var
    files = glob.glob(fpath)
    return files


def open_folder(window):
    folder_path = filedialog.askdirectory()
    if folder_path:
        window.folder_var = folder_path
        mp3_files = list_mp3_files(folder_path)
        if not mp3_files:
            tk.messagebox.showinfo("No mp3 file found", "No mp3 file was found in the provided directory")
            return
        for file in mp3_files:
            window.add_file_to_table(file)


def image_to_byte_array(image: Image) -> bytes:
    # BytesIO is a file-like buffer stored in memory
    imgbytearr = io.BytesIO()
    # image.save expects a file-like as an argument
    image.save(imgbytearr, format=image.format)
    # Turn the BytesIO object back into a bytes object
    imgbytearr = imgbytearr.getvalue()
    return imgbytearr


def save_metadata(window):
    msg_box = tk.messagebox.askyesno('Sauvegarder les modifications',
                                     'Êtes-vous sûr de vouloir sauvegarder vos modifications ?', icon='warning')
    if msg_box:
        for track_number in range(window.row_count):
            filename = window.table_values[track_number + 1]['Filename'].get("1.0", "end-1c")
            try:
                file = EasyID3()
                # metadata saving
                for head in window.technical_names_table:
                    file[head] = window.table_values[track_number + 1][head].get(
                        "1.0", "end-1c").strip()
                    # Save artist value also in performer to be compatible with more systems
                    if head == 'artist':
                        file['performer'] = window.table_values[track_number + 1][head].get("1.0", "end-1c").strip()
                file.save(window.folder_var + '/' + filename)
                # Image saving
                if track_number in window.original_image_table:
                    audio = ID3(window.folder_var + '/' + filename)
                    audio.delall('APIC')
                    audio.add(APIC(encoding=3, mime='image/jpeg', type=3,
                                   data=image_to_byte_array(window.original_image_table[track_number])))
                    audio.save(window.folder_var + '/' + filename, v2_version=3)
                # filename saving
                title = window.table_values[track_number + 1]['title'].get("1.0", "end-1c")
                if title:
                    if window.table_values[track_number + 1]['Filename'] != title.strip() + '.mp3':
                        os.rename(window.folder_var + '/' + filename, window.folder_var + '/' + title.strip() + '.mp3')
                        window.table_values[track_number + 1]['Filename'].config(state=tk.NORMAL)
                        window.table_values[track_number + 1]['Filename'].delete("1.0", tk.END)
                        window.table_values[track_number + 1]['Filename'].insert(tk.END, title.strip() + '.mp3')
                        window.table_values[track_number + 1]['Filename'].config(state=tk.DISABLED)
            except mutagen.MutagenError:
                tk.messagebox.showerror('File not found', 'File ' + filename + ' not found')

    return
