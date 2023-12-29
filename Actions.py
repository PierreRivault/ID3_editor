import io
import glob
import tkinter as tk
from tkinter import filedialog, messagebox


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


def image_to_byte_array(image):
    # BytesIO is a file-like buffer stored in memory
    imgbytearr = io.BytesIO()
    # image.save expects a file-like as an argument
    image.save(imgbytearr, format=image.format)
    # Turn the BytesIO object back into a bytes object
    imgbytearr = imgbytearr.getvalue()
    return imgbytearr
