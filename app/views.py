# STANDARD IMPORTS
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

import os
app = Flask(__name__)

# DIR TO SAVE IMAGES
app.config["MUSIC_UPLOADS"] = "/Users/arilybaert/Documents/gdm2/semester2/IOT-MakersLab/app/static/music/uploads"
app.config["ALLOWED_MUSIC_EXTENSIONS"] = ["MP3"]
app.config["ALLOWED_MUSIC_FILESIZE"] = 7496776

def allowed_music(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_MUSIC_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["ALLOWED_MUSIC_FILESIZE"]:
        return True
    else:
        return False

# HOME ROUTE
@app.route('/')
@app.route('/home')
def viewHome():
    return render_template("home.html");


# UPLOAD ROUTE
@app.route('/upload', methods=["GET", "POST"])
def upload_music():

    if request.method == 'POST':

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
                filename = secure_filename(music.filename)
            
            # SAVE FILE TO HDD
            music.save(os.path.join(app.config["MUSIC_UPLOADS"], filename))
            
            print("TUNE IS SAVED BRO")

            return redirect(request.url)

    # VIEW UPLOAD PAGE
    return render_template("upload.html");