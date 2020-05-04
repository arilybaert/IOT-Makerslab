# STANDARD IMPORTS
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

import os
import pygame
import json
import uuid 

app = Flask(__name__)

# DIR TO SAVE IMAGES
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

# PLAY MUSIC
def play_music(file):
    pygame.mixer.init()
    pygame.mixer.music.load(app.config["MUSIC_UPLOADS"] + file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue


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
            music.save(os.path.join(app.config["MUSIC_UPLOADS"], filename))
            
            print("TUNE IS SAVED BRO")

            return redirect(request.url)

    # VIEW UPLOAD PAGE
    return render_template("upload.html");

@app.route('/play', methods=["GET", "POST"])
def play_song():
    if request.method == 'POST':
        
        play_music(request.form['musicfilename'])
    
        
    #TO DO: MAKE MEDIA PLAYER
    filenames = os.listdir(app.config["MUSIC_UPLOADS"])

    return render_template("home.html", filenames= filenames);


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

