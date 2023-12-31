import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image


def set_global_genre(window):
    global_genre = window.global_genre_field.get()
    if global_genre:
        msg_box = tk.messagebox.askyesno('Définir un genre global',
                                         'Êtes vous sûr de vouloir définir le genre de tous les fichiers sur '
                                         + global_genre,
                                         icon='warning')
        if msg_box:
            # Check if the table is initiated
            if window.row_count > 0:
                for row_number in range(window.row_count):
                    window.table_values[row_number + 1]['genre'].delete("1.0", tk.END)
                    window.table_values[row_number + 1]['genre'].insert(tk.END, global_genre)
            else:
                tk.messagebox.showinfo('No folder loaded', 'Please open files before setting a global value')
    return


def set_global_album(window):
    global_album = window.global_album_field.get("1.0", "end-1c")
    if global_album:
        msg_box = tk.messagebox.askyesno('Définir un album global',
                                         'Êtes vous sûr de vouloir définir l\'album de tous les fichiers sur '
                                         + global_album,
                                         icon='warning')
        if msg_box:
            # Check if the table is initiated
            if window.row_count > 0:
                for row_number in range(window.row_count):
                    window.table_values[row_number + 1]['album'].delete("1.0", tk.END)
                    window.table_values[row_number + 1]['album'].insert(tk.END, global_album)
            else:
                tk.messagebox.showinfo('No folder loaded', 'Please open files before setting a global value')
    return


def set_global_date(window):
    global_date = window.global_date_field.get("1.0", "end-1c")
    if global_date:
        msg_box = tk.messagebox.askyesno('Définir une date globale',
                                         'Êtes vous sûr de vouloir définir la date de tous les fichiers sur '
                                         + global_date,
                                         icon='warning')
        if msg_box:
            # Check if the table is initiated
            if window.row_count > 0:
                for row_number in range(window.row_count):
                    window.table_values[row_number + 1]['date'].delete("1.0", tk.END)
                    window.table_values[row_number + 1]['date'].insert(tk.END, global_date)
            else:
                tk.messagebox.showinfo('No folder loaded', 'Please open files before setting a global value')
    return


def set_global_composer(window):
    global_composer = window.global_composer_field.get("1.0", "end-1c")
    if global_composer:
        msg_box = tk.messagebox.askyesno('Définir un compositeur global',
                                         'Êtes vous sûr de vouloir définir le compositeur de tous les fichiers sur '
                                         + global_composer,
                                         icon='warning')
        if msg_box:
            # Check if the table is initiated
            if window.row_count > 0:
                for row_number in range(window.row_count):
                    window.table_values[row_number + 1]['composer'].delete("1.0", tk.END)
                    window.table_values[row_number + 1]['composer'].insert(tk.END, global_composer)
            else:
                tk.messagebox.showinfo('No folder loaded', 'Please open files before setting a global value')
    return


def set_global_interpret(window):
    global_interpret = window.global_interpret_field.get("1.0", "end-1c")
    if global_interpret:
        msg_box = tk.messagebox.askyesno('Définir un interprète global',
                                         'Êtes vous sûr de vouloir définir l\'interprète de tous les fichiers sur '
                                         + global_interpret,
                                         icon='warning')
        if msg_box:
            # Check if the table is initiated
            if window.row_count > 0:
                for row_number in range(window.row_count):
                    window.table_values[row_number + 1]['artist'].delete("1.0", tk.END)
                    window.table_values[row_number + 1]['artist'].insert(tk.END, global_interpret)
            else:
                tk.messagebox.showinfo('No folder loaded', 'Please open files before setting a global value')
    return


# noinspection DuplicatedCode
def set_global_image(window):
    if window.global_image_path:
        try:
            global_image = Image.open(window.global_image_path)
            thumbnail = (global_image.resize((window.table_values[0]['Image'].winfo_width(),
                                              int(global_image.height * window.table_values[0][
                                                  'Image'].winfo_width() / global_image.width)),
                                             Image.BILINEAR))
            for row_number in range(window.row_count):
                window.original_image_table[row_number] = global_image
                window.image_table[row_number] = ImageTk.PhotoImage(thumbnail)
                # Remove old image from the GUI
                for children in window.table_values[row_number + 1]['image_container'].winfo_children():
                    children.destroy()
                window.table_values[row_number + 1]['Image'] = tk.Label(
                    window.table_values[row_number + 1]['image_container'],
                    image=window.image_table[row_number])
                window.table_values[row_number + 1]['Image'].grid(row=row_number + 1,
                                                                  column=len(window.columns_table))
        except IOError:
            tk.messagebox.showerror('Image not found', 'The global image provided was not found')
    else:
        tk.messagebox.showinfo('No global image provided',
                               'No global image is selected, please select one before proceeding')
    return


def choose_global_image(window):
    image_path = filedialog.askopenfilename(initialdir="D:/Musique/Icones")
    if image_path:
        window.global_image_path = image_path
        try:
            image = Image.open(image_path)
            image = image.resize(
                (int(image.width * window.top_frame.winfo_height() / image.height), window.top_frame.winfo_height()),
                Image.BILINEAR)
            window.global_image = ImageTk.PhotoImage(image)
            tk.Label(window.top_frame, image=window.global_image).grid(row=0, column=7, rowspan=2)
        except IOError:
            tk.messagebox.showerror('Image not found', 'The provided image could not be loaded')
    return


# noinspection DuplicatedCode
def change_image(window, index):
    image_path = filedialog.askopenfilename(initialdir="D:/Musique/Icones")
    if image_path:
        try:
            image = Image.open(image_path)
            window.original_image_table[index] = image
            thumbnail = (image.resize((window.table_values[0]['Image'].winfo_width(),
                                       int(image.height * window.table_values[0][
                                           'Image'].winfo_width() / image.width)), Image.BILINEAR))
            window.image_table[index] = ImageTk.PhotoImage(thumbnail)
            # Remove old image from the GUI
            for children in window.table_values[index + 1]['image_container'].winfo_children():
                children.destroy()
            window.table_values[index + 1]['Image'] = tk.Label(window.table_values[index + 1]['image_container'],
                                                               image=window.image_table[index])
            window.table_values[index + 1]['Image'].pack()
        except IOError:
            tk.messagebox.showerror('Image not found', 'The provided image could not be loaded')

    return
