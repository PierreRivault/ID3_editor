import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image

import Settings


def set_global_genre(window):
    global_genre = window.global_fields['genre'].get()
    if global_genre:
        msg_box = tk.messagebox.askyesno('Définir un genre global',
                                         'Êtes vous sûr de vouloir définir le genre de tous les fichiers sur '
                                         + global_genre,
                                         icon='warning')
        if msg_box:
            # Check if the table is initiated
            if window.row_count > 0:
                for row_number in range(window.row_count):
                    (window.Table.nametowidget('row' + str(row_number) + 'col' +
                                               str(window.technical_keys_table.index('TCON') + 2))
                     .delete("1.0", tk.END))
                    (window.Table.nametowidget('row' + str(row_number) + 'col' +
                                               str(window.technical_keys_table.index('TCON') + 2))
                     .insert(tk.END, global_genre))
            else:
                tk.messagebox.showinfo('Pas de fichier ouvert',
                                       'Veuillez ouvrir un fichier avant d\'appliquer un genre global')
    return


def set_global_album(window):
    global_album = window.global_fields['album'].get("1.0", "end-1c")
    if global_album:
        msg_box = tk.messagebox.askyesno('Définir un album global',
                                         'Êtes vous sûr de vouloir définir l\'album de tous les fichiers sur '
                                         + global_album,
                                         icon='warning')
        if msg_box:
            # Check if the table is initiated
            if window.row_count > 0:
                for row_number in range(window.row_count):
                    (window.Table.nametowidget('row' + str(row_number) + 'col' +
                                               str(window.technical_keys_table.index('TALB') + 2))
                     .delete("1.0", tk.END))
                    (window.Table.nametowidget('row' + str(row_number) + 'col' +
                                               str(window.technical_keys_table.index('TALB') + 2))
                     .insert(tk.END, global_album))
            else:
                tk.messagebox.showinfo('No folder loaded', 'Please open files before setting a global value')
    return


def set_global_date(window):
    global_date = window.global_fields['date'].get("1.0", "end-1c")
    if global_date:
        msg_box = tk.messagebox.askyesno('Définir une date globale',
                                         'Êtes vous sûr de vouloir définir la date de tous les fichiers sur '
                                         + global_date,
                                         icon='warning')
        if msg_box:
            # Check if the table is initiated
            if window.row_count > 0:
                for row_number in range(window.row_count):
                    (window.Table.nametowidget('row' + str(row_number) + 'col' +
                                               str(window.technical_keys_table.index('TDRC') + 2))
                     .delete("1.0", tk.END))
                    (window.Table.nametowidget('row' + str(row_number) + 'col' +
                                               str(window.technical_keys_table.index('TDRC') + 2))
                     .insert(tk.END, global_date))
            else:
                tk.messagebox.showinfo('No folder loaded', 'Please open files before setting a global value')
    return


def set_global_composer(window):
    global_composer = window.global_fields['composer'].get("1.0", "end-1c")
    if global_composer:
        msg_box = tk.messagebox.askyesno('Définir un compositeur global',
                                         'Êtes vous sûr de vouloir définir le compositeur de tous les fichiers sur '
                                         + global_composer,
                                         icon='warning')
        if msg_box:
            # Check if the table is initiated
            if window.row_count > 0:
                for row_number in range(window.row_count):
                    (window.Table.nametowidget('row' + str(row_number) + 'col' +
                                               str(window.technical_keys_table.index('TCOM') + 2))
                     .delete("1.0", tk.END))
                    (window.Table.nametowidget('row' + str(row_number) + 'col' +
                                               str(window.technical_keys_table.index('TCOM') + 2))
                     .insert(tk.END, global_composer))
            else:
                tk.messagebox.showinfo('No folder loaded', 'Please open files before setting a global value')
    return


def set_global_interpret(window):
    global_interpret = window.global_fields['interpret'].get("1.0", "end-1c")
    if global_interpret:
        msg_box = tk.messagebox.askyesno('Définir un interprète global',
                                         'Êtes vous sûr de vouloir définir l\'interprète de tous les fichiers sur '
                                         + global_interpret,
                                         icon='warning')
        if msg_box:
            # Check if the table is initiated
            if window.row_count > 0:
                for row_number in range(window.row_count):
                    (window.Table.nametowidget('row' + str(row_number) + 'col' +
                                               str(window.technical_keys_table.index('TPE1') + 2))
                     .delete("1.0", tk.END))
                    (window.Table.nametowidget('row' + str(row_number) + 'col' +
                                               str(window.technical_keys_table.index('TPE1') + 2))
                     .insert(tk.END, global_interpret))
            else:
                tk.messagebox.showinfo('No folder loaded', 'Please open files before setting a global value')
    return


# noinspection DuplicatedCode
def apply_global_image(window):
    if window.global_fields['image_path']:
        for row_number in range(window.row_count):
            window.add_image_to_row(row_number, window.global_fields['image_path'])
    else:
        tk.messagebox.showinfo('Pas d\'image globale sélectionnée',
                               'Aucune image n\'est sélectionnée, veuillez en choisir une avant de continuer')
    return


def choose_global_image(window):
    image_path = filedialog.askopenfilename(initialdir="D:/Musique/Icones")
    if image_path:
        window.global_fields['image_path'] = image_path
        try:
            image = Image.open(image_path)
            image = image.resize(
                (Settings.GLOBAL_IMAGE_WIDTH, int(Settings.GLOBAL_IMAGE_WIDTH * image.height / image.width)),
                Image.BILINEAR)
            window.global_image = ImageTk.PhotoImage(image)
            (tk.Label(window.root.nametowidget('left_frame'), image=window.global_image, name='global_image')
             .grid(row=11, column=0))
            window.root.nametowidget('left_frame.set_global_image').config(state=tk.NORMAL)
        except IOError:
            tk.messagebox.showerror('Image not found', 'The provided image could not be loaded')
    return


def change_image(window, index):
    image_path = filedialog.askopenfilename(initialdir="D:/Musique/Icones")
    if image_path:
        window.add_image_to_row(index, image_path)
