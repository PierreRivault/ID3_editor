import os
import re
import glob


from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from tkinter import Tk
from tkinter import filedialog

#TODO:  Lire la configuration du début depuis un settings.ini, et juste demander confirmation
#       (va probablement avec le premier point) revoir le code pour le simplifier

#Hides Tk base window
Tk().withdraw()

genre_table = ["Classique", "Video game Soundtrack", "Film Soundtrack", "Anime Soundtrack",
               "Song", "Epic Music", "Jazz", "National Anthem"]

global_vars = ["Genre", "Album", "Date", "Compositeur", "Interprète", "Image"]
global_vars_technical_names = ['genre', 'album', 'date', 'composer', 'performer', 'artist', 'tracknumber']
global_vars_status = [False for i in range(len(global_vars))]
global_vars_values = ["" for i in range(len(global_vars))]

loopvars = [True for i in range(7)]


# List all mp3 files from the current directory
path = os.getcwd()
fpath = u"%s/*.mp3" % path
files = glob.glob(fpath)

# Determine global values for the session
for i in range(len(global_vars)):
    while True:
        user_input = input("Le paramètre "+global_vars[i]+" doit-il être global?")
        if user_input != "oui" or user_input != "non" or user_input != "skip":
            break
    if user_input == "oui":
        global_vars_status[i] = True
        if i == 0:
            while True:
                input_value = input("Genre:")
                if input_value == "liste" or input_value == "Liste":
                    for elem in range(len(genre_table)):
                        print(elem, ":", genre_table[elem])
                elif input_value != "":
                    break
            try:
                global_vars_values[i] = genre_table[int(input_value)].strip()
                print(genre_table[int(input_value)])
            except ValueError:
                global_vars_values[i] = input_value.strip()
        elif i == 3 and global_vars_values[0] == "Classique":
            while True:
                input_value = input("Prénom:")
                global_composer_name = input("Nom:")
                if input_value != "" and global_composer_name != "":
                    break
            global_vars_values[i] = input_value + " " + global_composer_name
        elif i == 5:
            while global_vars_values[i] == "":
                global_vars_values[i] = filedialog.askopenfilename(initialdir="D:/Musique/Icones")
        else:
            while True:
                global_vars_values[i] = input("Valeur globale pour l'attribut' "+global_vars[i]+":")
                if global_vars_values[i] != "":
                    break
    elif user_input == "skip":
        global_vars_status[i] = True
        global_vars_values[i] = "skip"

#input tracknumbers/opus numbers or not
while True:
    need_number = input("Remplir les numéros de piste/d'opus dans la session?")
    if need_number == "oui" or need_number == "non":
        break
need_number = True if (need_number == "oui") else False

#input miniature or not
while True:
    need_picture = input("Ajouter une miniature aux fichiers?")
    if need_picture == "oui" or need_picture == "non":
        break
need_picture = True if need_picture == "oui" else False

#will only be used if there's no global picture
if need_picture:
    while True:
        global_auto_picture_classical = input("Toujours utiliser le nom du compositeur pour le genre Classique?")
        if global_auto_picture_classical != "oui" or global_auto_picture_classical != "non":
            break
    global_auto_picture_classical = True if global_auto_picture_classical == "oui" else False

#looping for each mp3 file
for fname in files:
    sname = os.path.basename(fname)
    step = 0
    while step < 7:
        if step == 0:
            _track = EasyID3(fname)
            #print file informations to the user
            os.system('cls')
            print(sname)
            print(_track.pprint())

            #Input for filename and title
            new_fname: str = input("Nom du fichier[" + sname + "]:")
            if new_fname == "skip":
                step += 1
                continue

            #if name is empty, keep the old one (can't be empty so no need for a loop)
            if new_fname == "":
                new_fname = sname
            if re.match(r".*\.mp3$", new_fname):
                new_fname = new_fname[0:len(new_fname)-4]
        elif step == 4 and _track['genre'][0] == "Classique":
            if global_vars_values[step-1] == "skip":
                step += 1
                continue
            if not global_vars_status[3]:
                if 'composer' in _track:
                    actual_var_value = _track['composer'][0]
                else:
                    actual_var_value = ""
                while True:
                    new_composer_fname = input("Prénom du compositeur[" + actual_var_value + "]:")
                    new_composer_sname = input("Nom du compositeur[" + actual_var_value + "]:")
                    if new_composer_fname != "" or new_composer_sname != "":
                        break
                    if new_composer_fname == "" and new_composer_sname == "" and actual_var_value != "":
                        break
                if new_composer_sname == "" and new_composer_fname == "":
                    _track['composer'] = actual_var_value.strip()
                    actual_composer_sname = input("Entrer uniquement le nom du compositeur actuel[" + actual_var_value + "]:")
                    if not re.match(r"^"+actual_composer_sname+" -.*$", new_fname) and _track['genre'][0] == "Classique":
                        new_fname = (actual_composer_sname + " - " if actual_composer_sname != "" else "") + new_fname
                elif new_composer_fname == "Back" or new_composer_sname == "Back":
                    step -= 1
                    while global_vars_status[step-1] == True:
                        step -= 1
                    continue
                else:
                    _track['composer'] = (new_composer_fname + " " + new_composer_sname).strip()
                    if not re.match(r"^"+new_composer_sname+" -.*$", new_fname) and _track['genre'][0] == "Classique":
                        new_fname = (new_composer_sname + " - " if new_composer_sname != "" else "") + new_fname
            else:
                _track['composer'] = global_vars_values[3].strip()
                if not re.match(r"^"+global_composer_name+" -.*$", new_fname) and _track['genre'][0] == "Classique":
                    new_fname = (global_composer_name + " - " if global_composer_name != "" else "") + new_fname
        elif step == 5:
            if global_vars_values[step-1] == "skip":
                step += 1
                continue
            if not global_vars_status[4]:
                if 'artist' in _track and 'performer' in _track:
                    if _track['artist'][0] != _track['performer'][0]:
                        while True:
                            print("L'artiste et l'interprète présents sont différents:\n"
                                "Artiste:"+_track['artist'][0]+"\n"
                                                                "Interprète:"+_track['performer'][0])
                            choix_aa = input("Conserver l'artiste(1), l'interprète(2) ou aucun des deux(0)?")
                            if choix_aa == "0":
                                actual_performer = ""
                                break
                            elif choix_aa == "1":
                                actual_performer = _track['artist'][0]
                                break
                            elif choix_aa == "2":
                                actual_performer = _track['performer'][0]
                                break
                    else:
                        actual_performer = _track['performer'][0]
                else:
                    if 'artist' in _track:
                        actual_performer = _track['artist'][0]
                    elif 'performer' in _track:
                        actual_performer = _track['performer'][0]
                    else:
                        actual_performer = ""

                while True:
                    new_var_value = input("Nom de l'interprète[" + actual_performer + "]:")
                    if new_var_value != "":
                        break
                    if new_var_value == "" and actual_performer != "":
                        break
                if new_var_value == "":
                    _track['artist'] = actual_performer.strip()
                    _track['performer'] = actual_performer.strip()
                elif new_var_value == "Back":
                    step -= 1
                    while global_vars_status[step-1] == True:
                        step -= 1
                    continue
                else:
                    _track['artist'] = new_var_value.strip()
                    _track['performer'] = new_var_value.strip()
            else:
                _track['artist'] = global_vars_values[4].strip()
                _track['performer'] = global_vars_values[4].strip()
        elif step == 6:
            if need_number:
                if 'tracknumber' in _track:
                    actual_tnumber = _track['tracknumber'][0]
                else:
                    actual_tnumber = ""
                new_tnumber = input("Numéro de piste/d'opus[" + actual_tnumber + "]:")
                if new_tnumber == "":
                    _track['tracknumber'] = actual_tnumber.strip()
                elif new_tnumber == "Back":
                    step -= 1
                    while global_vars_status[step-1] == True:
                        step -= 1
                    continue
                else:
                    _track['tracknumber'] = new_tnumber.strip()
        else:
            if global_vars_values[step-1] == "skip":
                step += 1
                continue
            if not global_vars_status[step - 1]:
                if global_vars_technical_names[step-1] in _track:
                    actual_var_value = _track[global_vars_technical_names[step-1]][0]
                else:
                    actual_var_value = ""
                while True:
                    new_var_value = input("Valeur pour l'attribut "+global_vars[step-1]+" ["+actual_var_value+"]:")
                    if new_var_value == "Liste" and step == 1 or new_var_value == "liste" and step == 1:
                        for elem in range(len(genre_table)):
                            print(elem, ":", genre_table[elem])
                    elif new_var_value != "":
                        break
                    elif new_var_value == "" and actual_var_value != "":
                        break
                if new_var_value == "":
                    _track[global_vars_technical_names[step-1]] = actual_var_value.strip()
                elif new_var_value == "Back":
                    step -= 1
                    if step > 0:
                        while global_vars_status[step-1] == True:
                            step -= 1
                    continue
                else:
                    if step == 1:
                        try:
                            _track['genre'] = genre_table[int(new_var_value)].strip()
                            print(genre_table[int(new_var_value)])
                        except ValueError:
                            _track['genre'] = new_var_value.strip()
                    else:
                        _track[global_vars_technical_names[step-1]] = new_var_value.strip()
            else:
                _track[global_vars_technical_names[step-1]] = global_vars_values[step-1].strip()
        step += 1

    #Saves the metadata before opening the file again for adding an image
    _track['title'] = new_fname.strip()
    _track.save()

    #Cover management
    if need_picture:
        new_icone = ""
        if not global_vars_status[5]:
            user_input = ""
            if _track['genre'][0] == "Classique":
                if not global_auto_picture_classical:
                    while user_input != "oui" and user_input != "non":
                        user_input = input("Utiliser le nom du compositeur?")
                if user_input == "oui" or global_auto_picture_classical:
                    if os.path.exists("D:/Musique/Icones/"+_track['composer'][0]+'.jpg'):
                        new_icone = "D:/Musique/Icones/"+_track['composer'][0]+".jpg"
            while new_icone == "":
                new_icone = filedialog.askopenfilename(initialdir="D:/Musique/Icones")
        else:
            new_icone = global_vars_values[5]
        
        audio = ID3(fname)
        with open(new_icone, 'rb') as albumart:
            audio.add(APIC(encoding = 3, mime = 'image/jpeg', type = 3, desc = u'Cover', data = albumart.read()))
        audio.save(v2_version = 3)


    #Finally renames the file with the correct filename
    if new_fname != "":
        os.rename(fname, new_fname.strip() + ".mp3")
