import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkintertable import TableCanvas


def set_global_genre(window):
    global_genre = window.global_genre_field.get()
    if global_genre:
        msg_box = tk.messagebox.askyesno('Définir un genre global',
                                         'Êtes vous sûr de vouloir définir le genre de tous les fichiers sur ' + global_genre,
                                         icon='warning')
        if msg_box:
            # Check if the table is initiated
            if hasattr(window.table, 'tablerowheader') and hasattr(window.table, 'tablecolheader'):
                for row_number in range(window.model.getRowCount()):
                    window.model.data[window.model.getRecName(row_number).strip()][
                        window.columns_table[2]] = global_genre
                window.table.redrawTable()
    return


def set_global_album(window):
    global_album = window.global_album_field.get("1.0", "end-1c")
    if global_album:
        msg_box = tk.messagebox.askyesno('Définir un album global',
                                         'Êtes vous sûr de vouloir définir l\'album de tous les fichiers sur ' + global_album,
                                         icon='warning')
        if msg_box:
            # Check if the table is initiated
            if hasattr(window.table, 'tablerowheader') and hasattr(window.table, 'tablecolheader'):
                for row_number in range(window.model.getRowCount()):
                    window.model.data[window.model.getRecName(row_number).strip()][
                        window.columns_table[3]] = global_album
                window.table.redrawTable()
    return


def set_global_date(window):
    global_date = window.global_date_field.get("1.0", "end-1c")
    if global_date:
        msg_box = tk.messagebox.askyesno('Définir une date globale',
                                         'Êtes vous sûr de vouloir définir la date de tous les fichiers sur ' + global_date,
                                         icon='warning')
        if msg_box:
            # Check if the table is initiated
            if hasattr(window.table, 'tablerowheader') and hasattr(window.table, 'tablecolheader'):
                for row_number in range(window.model.getRowCount()):
                    window.model.data[window.model.getRecName(row_number).strip()][
                        window.columns_table[4]] = global_date
                window.table.redrawTable()
    return


def set_global_composer(window):
    global_composer = window.global_composer_field.get("1.0", "end-1c")
    if global_composer:
        msg_box = tk.messagebox.askyesno('Définir un compositeur global',
                                         'Êtes vous sûr de vouloir définir le compositeur de tous les fichiers sur ' + global_composer,
                                         icon='warning')
        if msg_box:
            # Check if the table is initiated
            if hasattr(window.table, 'tablerowheader') and hasattr(window.table, 'tablecolheader'):
                for row_number in range(window.model.getRowCount()):
                    window.model.data[window.model.getRecName(row_number).strip()][
                        window.columns_table[5]] = global_composer
                window.table.redrawTable()
    return


def set_global_interpret(window):
    global_interpret = window.global_interpret_field.get("1.0", "end-1c")
    if global_interpret:
        msg_box = tk.messagebox.askyesno('Définir un interprète global',
                                         'Êtes vous sûr de vouloir définir l\'interprète de tous les fichiers sur ' + global_interpret,
                                         icon='warning')
        if msg_box:
            # Check if the table is initiated
            if hasattr(window.table, 'tablerowheader') and hasattr(window.table, 'tablecolheader'):
                for row_number in range(window.model.getRowCount()):
                    window.model.data[window.model.getRecName(row_number).strip()][
                        window.columns_table[6]] = global_interpret
                window.table.redrawTable()
    return


def set_global_image(window):
    return


def choose_global_image(window):
    return
