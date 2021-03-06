from flask import Flask, jsonify, request
import sys
import os
from db import create_tables
import artist, album, track
import sqlite3

# Para este ejemplo pediremos la id
# y no la generaremos automáticamente
# USER_KEYS = ['uid', 'name', 'age',
#             'description']
# MESSAGE_KEYS = ['message', 'sender', 'receptant', 'lat', 'long', 'date']
# TEXT_KEYS = ['required', 'desired', 'forbidden', 'userId']


create_tables()
# Iniciamos la aplicación de flask
app = Flask(__name__)

@app.route("/")
def home():
    '''
    Página de inicio
    '''
    return "<h1>¡Bienvenido a la API de música!</h1>"

"""
TODOS LO METODOS GET
"""

@app.route('/artists', methods=["GET"])
def get_artists():
    artists, codigo = artist.get_artists()
    return jsonify(artists), codigo

@app.route("/artists/<id>", methods=["GET"])
def get_artist_by_id(id):
    artists, codigo = artist.get_by_id(id)
    return jsonify(artists), codigo

@app.route("/artists/<id>/albums", methods=["GET"])
def get_artist_albums_by_id(id):
    albums, codigo = artist.get_artists_albums_by_id(id)
    return jsonify(albums), codigo

@app.route("/artists/<id>/tracks", methods=["GET"])
def get_artist_tracks_by_id(id):
    tracks, codigo = artist.get_artists_tracks_by_id(id)
    return jsonify(tracks), codigo

@app.route('/albums', methods=["GET"])
def get_albums():
    albums, codigo = album.get_albums()
    return jsonify(albums), codigo

@app.route("/albums/<id>", methods=["GET"])
def get_album_by_id(id):
    albums, codigo = album.get_by_id(id)
    return jsonify(albums), codigo

@app.route("/albums/<id>/tracks", methods=["GET"])
def get_album_tracks_by_id(id):
    tracks, codigo = album.get_album_tracks_by_id(id)
    return jsonify(tracks), codigo

@app.route('/tracks', methods=["GET"])
def get_tracks():
    tracks, codigo = track.get_tracks()
    return jsonify(tracks), codigo

@app.route("/tracks/<id>", methods=["GET"])
def get_track_by_id(id):
    tracks, codigo = track.get_by_id(id)
    return jsonify(tracks), codigo


"""
TODOS LO METODOS POST
"""


@app.route("/artists", methods=["POST"])
def insert_artist():
    artist_details = request.get_json()
    if type(artist_details) == type(None) or artist_details == {}:
        name = None
        age = None
    else:
        try: 
            name = artist_details["name"]
        except:
            name = None
        try: 
            age = artist_details["age"]
        except:
            age = None
    print(request.args.get("name"))
    print(age)
    result, codigo = artist.insert_artist(name, age)
    return jsonify(result), codigo

@app.route("/artists/<id>/albums", methods=["POST"])
def insert_album(id):
    album_details = request.get_json()
    if type(album_details) == type(None) or album_details == {}:
        name = None
        genre = None
    else:
        try: 
            name = album_details["name"]
        except:
            name = None
        try:
            genre = album_details["genre"]
        except:
            genre = None
    result, codigo = album.insert_album(id, name, genre)
    return jsonify(result), codigo

@app.route("/albums/<id>/tracks", methods=["POST"])
def insert_track(id):
    track_details = request.get_json()
    if type(track_details) == type(None) or track_details == {}:
        name = None
        duration = None
    else:
        try:
            name = track_details["name"]
        except:
            name = None
        try:
            duration = track_details["duration"]
        except:
            duration = None
    result, codigo = track.insert_track(id, name, duration)
    return jsonify(result), codigo



"""
TODOS LO METODOS DELETE
"""

@app.route("/artists/<id>", methods=["DELETE"])
def delete_artist(id):
    result, codigo = artist.delete_artist(id)
    return jsonify(result), codigo

@app.route("/albums/<id>", methods=["DELETE"])
def delete_album(id):
    result, codigo = album.delete_album(id)
    return jsonify(result), codigo

@app.route("/tracks/<id>", methods=["DELETE"])
def delete_track(id):
    result, codigo = track.delete_track(id)
    return jsonify(result), codigo


"""
TODOS LO METODOS PUT
"""


@app.route("/artists/<id>/albums/play", methods=["PUT"])
def play_tracks_artist(id):
    result, codigo = artist.play_tracks(id)
    return jsonify(result), codigo

@app.route("/albums/<id>/tracks/play", methods=["PUT"])
def play_tracks_album(id):
    result, codigo = album.play_tracks(id)
    return jsonify(result), codigo

@app.route("/tracks/<id>/play", methods=["PUT"])
def play_tracks(id):
    result, codigo = track.play_tracks(id)
    return jsonify(result), codigo

"""
TODOS LOS INCORRECTOS
"""

@app.route('/artists', methods=["DELETE", "PUT", "PATCH", "COPY", "HEAD", "OPTIONS", "LINK", "UNLINK", "PURGE", "LOCK", "UNLOCK", "PROPFIND", "VIEW" ])
def wrong_method_1():
    return jsonify("Wrong method"), 405

@app.route("/artists/<id>", methods=["POST", "PUT", "PATCH", "COPY", "HEAD", "OPTIONS", "LINK", "UNLINK", "PURGE", "LOCK", "UNLOCK", "PROPFIND", "VIEW" ])
def wrong_method_2():
    return jsonify("Wrong method"), 405

@app.route("/artists/<id>/albums", methods=["DELETE", "PUT", "PATCH", "COPY", "HEAD", "OPTIONS", "LINK", "UNLINK", "PURGE", "LOCK", "UNLOCK", "PROPFIND", "VIEW" ])
def wrong_method_3():
    return jsonify("Wrong method"), 405

@app.route("/artists/<id>/tracks", methods=["POST", "DELETE", "PUT", "PATCH", "COPY", "HEAD", "OPTIONS", "LINK", "UNLINK", "PURGE", "LOCK", "UNLOCK", "PROPFIND", "VIEW" ])
def wrong_method_4():
    return jsonify("Wrong method"), 405

@app.route('/albums', methods=["POST", "DELETE", "PUT", "PATCH", "COPY", "HEAD", "OPTIONS", "LINK", "UNLINK", "PURGE", "LOCK", "UNLOCK", "PROPFIND", "VIEW" ])
def wrong_method_5():
    return jsonify("Wrong method"), 405

@app.route("/albums/<id>", methods=["POST", "PUT","PATCH", "COPY", "HEAD", "OPTIONS", "LINK", "UNLINK", "PURGE", "LOCK", "UNLOCK", "PROPFIND", "VIEW" ])
def wrong_method_6():
    return jsonify("Wrong method"), 405

@app.route("/albums/<id>/tracks", methods=["DELETE", "PUT", "PATCH", "COPY", "HEAD", "OPTIONS", "LINK", "UNLINK", "PURGE", "LOCK", "UNLOCK", "PROPFIND", "VIEW" ])
def wrong_method_7():
    return jsonify("Wrong method"), 405

@app.route('/tracks', methods=["POST", "DELETE", "PUT", "PATCH", "COPY", "HEAD", "OPTIONS", "LINK", "UNLINK", "PURGE", "LOCK", "UNLOCK", "PROPFIND", "VIEW" ])
def wrong_method_8():
    return jsonify("Wrong method"), 405

@app.route("/tracks/<id>", methods=["POST",  "PUT", "PATCH", "COPY", "HEAD", "OPTIONS", "LINK", "UNLINK", "PURGE", "LOCK", "UNLOCK", "PROPFIND", "VIEW" ])
def wrong_method_9():
    return jsonify("Wrong method"), 405

@app.route("/artists/<id>/albums/play", methods=["GET", "POST", "DELETE", "PATCH", "COPY", "HEAD", "OPTIONS", "LINK", "UNLINK", "PURGE", "LOCK", "UNLOCK", "PROPFIND", "VIEW" ])
def wrong_method_10():
    return jsonify("Wrong method"), 405

@app.route("/albums/<id>/tracks/play", methods=["GET", "POST", "DELETE", "PATCH", "COPY", "HEAD", "OPTIONS", "LINK", "UNLINK", "PURGE", "LOCK", "UNLOCK", "PROPFIND", "VIEW" ])
def wrong_method_11():
    return jsonify("Wrong method"), 405

@app.route("/tracks/<id>/play", methods=["GET", "POST", "DELETE", "PATCH", "COPY", "HEAD", "OPTIONS", "LINK", "UNLINK", "PURGE", "LOCK", "UNLOCK", "PROPFIND", "VIEW" ])
def wrong_method_12():
    return jsonify("Wrong method"), 405


if __name__ == "__main__":
    app.run(debug=True)