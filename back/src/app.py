from flask import Flask, request
from json import loads, dumps
import os
from playlist.parser import run
from playlist.upload import main

app = Flask(__name__)

@app.route("/")
def index():
    return dumps("Index endpoint")

@app.route("/find_path", methods=["GET"])
def find_path():
    try:
        path = request.json['path']
        print(os.listdir(path))
        return {"message": "Success"}, 200
    except:
        return {"message": "Path doesn't exist"}, 404
    
@app.route("/playlist_parser", methods=["GET"])
def playlist_parser():
    try:
        path = request.json['path']
        run(path)
        with open("playlist.json", "r") as file:
            file = loads(file.read())

        return file, 200
    except:
        return {"message": "Error while parsing playlists"}, 500

@app.route("/playlist_upload", methods=["GET"])
def playlist_upload():
    try:
        main()
        return {"message": "Success"}, 200
    except Exception as e:
        return {"message": f"Error while sending videos to youtube: {e}"}, 500