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


def init_window(window):
    window.root.title("MP3 Editor")
    window.root.geometry('1280x720')

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
    window.top_frame = tk.Frame(window.root)
    window.top_frame.grid(row=0, column=0, sticky='nsew')

    # Create the second frame
    window.middle_frame = tk.Frame(window.root)
    window.middle_frame.grid(row=1, column=0, sticky='nsew')

    # Create the third frame
    window.bottom_frame = tk.Frame(window.root)
    window.bottom_frame.grid(row=2, column=0, sticky='nsew')

    # Create elements of the first frame, global values
    window.top_frame.grid_columnconfigure(0, weight=1)
    window.top_frame.grid_columnconfigure(8, weight=1)
    # Genre field and button
    window.global_genre_field = ttk.Combobox(window.top_frame, values=window.genre_table)
    window.global_genre_field.current(0)
    window.global_genre_field.grid(column=1, row=0, padx=10, pady=10, sticky="we")
    global_genre_button = tk.Button(window.top_frame, text='Définir le genre global',
                                    command=lambda: Commands.set_global_genre(window))
    global_genre_button.grid(column=1, row=1, padx=10, pady=10)
    # Album field and button
    window.global_album_field = tk.Text(window.top_frame, height=1, width=10)
    window.global_album_field.grid(column=2, row=0, padx=10, pady=10, sticky="we")
    global_album_button = tk.Button(window.top_frame, text='Définir l\'album global',
                                    command=lambda: Commands.set_global_album(window))
    global_album_button.grid(column=2, row=1, padx=10, pady=10)
    # Date field and button
    window.global_date_field = tk.Text(window.top_frame, height=1, width=10)
    window.global_date_field.grid(column=3, row=0, padx=10, pady=10, sticky="we")
    global_date_button = tk.Button(window.top_frame, text='Définir la date globale',
                                   command=lambda: Commands.set_global_date(window))
    global_date_button.grid(column=3, row=1, padx=10, pady=10)
    # Composer field and button
    window.global_composer_field = tk.Text(window.top_frame, height=1, width=10)
    window.global_composer_field.grid(column=4, row=0, padx=10, pady=10, sticky="we")
    global_composer_button = tk.Button(window.top_frame, text='Définir le compositeur global',
                                       command=lambda: Commands.set_global_composer(window))
    global_composer_button.grid(column=4, row=1, padx=10, pady=10)
    # Interpret field and button
    window.global_interpret_field = tk.Text(window.top_frame, height=1, width=10)
    window.global_interpret_field.grid(column=5, row=0, padx=10, pady=10, sticky="we")
    global_interpret_button = tk.Button(window.top_frame, text='Définir l\'interprète global',
                                        command=lambda: Commands.set_global_interpret(window))
    global_interpret_button.grid(column=5, row=1, padx=10, pady=10)
    # Image choosing and setting button
    global_image_choosing_button = tk.Button(window.top_frame, text='Choisir l\'image globale',
                                             command=lambda: Commands.choose_global_image(window))
    global_image_choosing_button.grid(column=6, row=0, padx=10, pady=10)
    global_image_setting_button = tk.Button(window.top_frame, text='Définir l\'image globale',
                                            command=lambda: Commands.set_global_image(window))
    global_image_setting_button.grid(column=6, row=1, padx=10, pady=10)
    # End of the first frame

    # Create elements of the second frame
    # Create the canvas
    window.canvas = tk.Canvas(window.middle_frame)
    # Create the scrollbar
    window.scrollbar = tk.Scrollbar(window.middle_frame, orient=tk.VERTICAL)
    # Pack the scrollbar on the right
    window.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    # Config the scrollbar
    window.scrollbar.config(command=window.canvas.yview)
    # Bind the scrollbar to the canvas
    window.canvas.configure(yscrollcommand=window.scrollbar.set)
    # Pack the canvas
    window.canvas.pack(fill=tk.BOTH, expand=True)
    # Create the frame in the canvas
    window.canvas_frame = tk.Frame(window.canvas, width=window.root.winfo_screenwidth()-window.scrollbar.winfo_width())
    window.canvas_frame.pack(fill=tk.BOTH, expand=True)
    # Create the canvas view window
    window.frame_id = window.canvas.create_window((0, 0), window=window.canvas_frame, anchor='nw')

    # Bind events on canvas resizing
    window.canvas_frame.bind('<Configure>', window.on_configure)
    window.canvas.bind('<Configure>', window.on_canvas_configure)

    # Set grid weights
    for index in range(len(window.columns_table_weight)):
        window.canvas_frame.grid_columnconfigure(index, weight=window.columns_table_weight[index], uniform='1')
    # Create the table headers
    table_headers = {}
    for index, head_name in enumerate(window.columns_table):
        table_headers[head_name] = ttk.Label(window.canvas_frame, text=window.columns_table[index], relief='solid')
        table_headers[head_name].configure(anchor="center")
        table_headers[head_name].grid(column=index + 1, row=0, sticky='ew')
    window.table_values[0] = table_headers
    # End of the second frame

    # Create elements of the third frame, commands
    save_button = tk.Button(window.bottom_frame, text="Sauvegarder", command=lambda: save_metadata(window))
    save_button.pack()

    # Create keyboard shortcuts
    window.root.bind("<Control-o>", lambda e: open_folder(window))
    window.root.bind("<Control-s>", lambda e: save_metadata(window))
    window.root.bind("<Configure>", window.on_window_resize)

    return window


def list_mp3_files(folder_var):
    fpath = u"%s/*.mp3" % folder_var
    files = glob.glob(fpath)
    return files


def create_table(window):
    # List mp3 files in the folder
    mp3_files = list_mp3_files(window.folder_var)

    if not mp3_files:
        tk.messagebox.showinfo("No mp3 file found", "No mp3 file was found in the provided directory")
        return

    window.row_count = 0

    for index, file in enumerate(mp3_files):
        try:
            _track = EasyID3(file)
        except ID3NoHeaderError:
            _track = EasyID3()
        table_row = {}
        # Load metadata included in technical_names_table
        for head_index, head_name in enumerate(window.technical_names_table):
            table_row[head_name] = tk.Text(window.canvas_frame, height=1, width=1)
            table_row[head_name].grid(row=index + 1, column=head_index + 2, sticky='ew')
            table_row[head_name].insert(tk.END, _track[window.technical_names_table[head_index]][0] if
                                        window.technical_names_table[head_index] in _track else '')
            # table_row[head_name].bind('<Tab>', window.focus_next_widget)
        # Load image
        table_row['image_container'] = tk.Frame(window.canvas_frame,
                                                width=window.table_values[0]['Image'].winfo_width())
        table_row['image_container'].grid(row=index + 1, column=len(window.columns_table))
        table_row['image_container'].grid_propagate(False)
        try:
            audio = ID3(file)
        except ID3NoHeaderError:
            audio = ID3()
        if audio.get("APIC:"):
            raw_album = audio.get("APIC:").data
            window.original_image_table[index] = Image.open(BytesIO(raw_album))
            album = (window.original_image_table[index].resize(
                (window.table_values[0]['Image'].winfo_width(),
                 int(window.original_image_table[index].height * window.table_values[0]['Image'].winfo_width() /
                     window.original_image_table[index].width)),
                Image.BILINEAR))
            window.image_table[index] = ImageTk.PhotoImage(album)
            table_row['image'] = tk.Label(table_row['image_container'], image=window.image_table[index])
            table_row['image'].pack()
        # Add index
        table_row['Index'] = tk.Text(window.canvas_frame, height=1, width=1)
        table_row['Index'].grid(row=index + 1, column=0, sticky='ew')
        table_row['Index'].insert(tk.END, str(index + 1))
        table_row['Index'].config(state=tk.DISABLED)
        # Add filename
        table_row['Filename'] = tk.Text(window.canvas_frame, height=1, width=1)
        table_row['Filename'].grid(row=index + 1, column=1, sticky='ew')
        table_row['Filename'].insert(tk.END, os.path.basename(file))
        table_row['Filename'].config(state=tk.DISABLED)
        # Add change image button
        table_row['Change_image'] = tk.Button(window.canvas_frame, text='Change',
                                              command=lambda image_index=index: Commands.change_image(window,
                                                                                                      image_index))
        table_row['Change_image'].grid(row=index + 1, column=len(window.columns_table) + 1)
        window.table_values[index + 1] = table_row
        window.row_count += 1
    return


def open_folder(window):
    folder_path = filedialog.askdirectory()
    if folder_path:
        window.folder_var = folder_path
        # Call create_table after setting folder_var
        create_table(window)


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
