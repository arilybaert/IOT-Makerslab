# STANDARD IMPORTS
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from js.jquery import jquery
from classes.player import Player
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

import cgi, cgitb
import os
import pygame
import json
import uuid 
import unicodedata

app = Flask(__name__)
sense = SenseHat()
PyPlayer = Player()

jquery.need()
sense.clear()



def pushed_up(event):
    if event.action != ACTION_RELEASED:
    	PyPlayer.stop_music()
def pushed_down(event):
    if event.action != ACTION_RELEASED:
    	PyPlayer.start_music()

sense.stick.direction_up = pushed_up
sense.stick.direction_down = pushed_down



# CONSTS
app.config["MUSIC_UPLOADS"] = "/home/pi/Documents/IOT-Makerslab/app/static/music/uploads/"
app.config["MUSIC_METADATA"] = "static/music/metadata/metadata.txt"
app.config["ALLOWED_MUSIC_EXTENSIONS"] = ["MP3"]
app.config["ALLOWED_MUSIC_FILESIZE"] = 7496776

#
# FUNCTIONS
#

# CHECK EXTENSIONS
def allowed_music(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_MUSIC_EXTENSIONS"]:
        return True
    else:
        return False

# CHECK FILESIZE
def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["ALLOWED_MUSIC_FILESIZE"]:
        return True
    else:
        return False


#
# ROUTES:
#

# HOME ROUTE
@app.route('/')
@app.route('/home')
def viewHome():
    filenames = os.listdir(app.config["MUSIC_UPLOADS"])
    with open(app.config["MUSIC_METADATA"]) as json_file:
            data = json.load(json_file)
    return render_template("home.html", filenames= filenames, metadata= data);


# UPLOAD ROUTE
@app.route('/upload', methods=["GET", "POST"])
def upload_music():

    if request.method == 'POST':
        
        unid = uuid.uuid1()

        print(request.form['songTitle'])
        print(request.form['songArtist'])
        print(request.form['songArtwork'])
        with open(app.config["MUSIC_METADATA"]) as json_file:
            data = json.load(json_file)

        data['music'].append({
            'title': request.form['songTitle'],
            'artist': request.form['songArtist'],
            'artwork': request.form['songArtwork'],
            'id': str(unid.int)
        })
        with open(app.config["MUSIC_METADATA"], 'w') as outfile:
            json.dump(data, outfile)
        
        #return redirect(request.url)
        
        if request.files:
            if not allowed_image_filesize(request.cookies.get("filesize")):
                print("file exceeded max size")
                return redirect(request.url)

            music = request.files["music"]

            # FILE MUST CONTAIN NAME
            if music.filename == "":
                print("file needs filename")
                return redirect(request.url)
            
            # FILE MUST HAVE RIGHT EXTENSION
            if not allowed_music(music.filename):
                print("file extension is not allowed")
                return redirect(request.url)
            else:
                filename = str(unid.int) + ".mp3"
                print(filename)
            
            # SAVE FILE TO HDD
            music.save(os.path.join(app.config["MUSIC_UPLOADS"], filename, ))
            
            print("TUNE IS SAVED BRO")

            return redirect(request.url)

    # VIEW UPLOAD PAGE
    return render_template("upload.html");


@app.route('/play', methods=["GET", "POST"])
def play_song():
    # print("busy: " + str(pygame.mixer.music.get_busy()))
    if request.method == 'POST':
        PyPlayer.start_next_song(app.config["MUSIC_UPLOADS"] + request.form['musicfilename'])

        
    filenames = os.listdir(app.config["MUSIC_UPLOADS"])
    with open(app.config["MUSIC_METADATA"]) as json_file:
            data = json.load(json_file)
    return render_template("home.html", filenames= filenames, metadata= data);


@app.route('/pause')
def pause():
    PyPlayer.stop_music()
    
    filenames = os.listdir(app.config["MUSIC_UPLOADS"])
    with open(app.config["MUSIC_METADATA"]) as json_file:
            data = json.load(json_file)
    return render_template("home.html", filenames= filenames, metadata= data);


@app.route('/unpause')
def unpause():
    PyPlayer.start_music()
    
    filenames = os.listdir(app.config["MUSIC_UPLOADS"])
    with open(app.config["MUSIC_METADATA"]) as json_file:
            data = json.load(json_file)
    return render_template("home.html", filenames= filenames, metadata= data);


@app.route('/volume', methods=["GET", "POST"])
def volume():

    if request.method == 'POST':
        volume = request.form["volume"]
        volume = int(volume)

        PyPlayer.set_volume(volume)


    filenames = os.listdir(app.config["MUSIC_UPLOADS"])
    with open(app.config["MUSIC_METADATA"]) as json_file:
            data = json.load(json_file)
    return render_template("home.html", filenames= filenames, metadata= data);




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

