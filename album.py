from db import get_db
from base64 import b64encode

def get_albums():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id, artist_id, name, genre, artist, tracks, self FROM album"
    cursor.execute(query)
    albums_lista = []
    albums = cursor.fetchall()
    for a in albums:
        albums_lista.append({"id": a[0], "artist_id": a[1], "name": a[2], "genre": a[3], "artist": a[4], "tracks": a[5], "self": a[5]})
    return albums_lista, 200 

def get_by_id(id_album):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, artist_id, name, genre, artist, tracks, self FROM album WHERE id = ?"
    cursor.execute(statement, [id_album])
    album = cursor.fetchone()
    albums_lista = {"id": album[0], "artist_id": album[1], "name": album[2], "genre": album[3], "artist": album[4], "tracks": album[5], "self": album[6]}
    return albums_lista, 200 

def get_album_tracks_by_id(id_album):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, album_id, name, duration, times_played, artist, album, self FROM track WHERE id_album = ?"
    cursor.execute(statement, [id_album])
    tracks_lista = []
    tracks = cursor.fetchall()
    for a in tracks:
        tracks_lista.append({"id": a[0], "album_id": a[1], "name": a[2], "duration": a[3], "times_played": a[4], "artist": a[5], "album": a[6], "self": a[7]})
    return tracks_lista, 200


def insert_album(id_artist, name, genre):
    db = get_db()
    cursor = db.cursor()
    id_album = b64encode(name.encode()).decode('utf-8')
    if len(id_album) >= 22:
        id_album = id_album[:22]
    statement = "INSERT INTO album(id, artist_id, name, genre, artist, tracks, self) VALUES (?, ?, ?, ?, ?, ?, ?)"
    artist = f"https://t2-tdi.herokuapp.com/artists/{id_artist}"
    tracks = f"https://t2-tdi.herokuapp.com/albums/{id_album}/tracks"
    self_page = f"https://t2-tdi.herokuapp.com/albums/{id_album}"
    cursor.execute(statement, [id_album, id_artist, name, genre, artist, tracks, self_page])
    db.commit()
    return {"id": id_album, "id_artist": id_artist, "name": name, "age": genre, "artist": artist, "tracks": tracks, "self": self_page}, 201

def delete_album(id_album):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM album WHERE id = ?"
    cursor.execute(statement, [id_album])
    db.commit()
    return "Album borrado", 204

def play_tracks(id_album):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id FROM track WHERE id_album = ?"
    cursor.execute(statement, [id_album])
    track_album = cursor.fetchall()
    for track in track_album:
        statement = "SELECT times_played FROM track WHERE id = ?"
        cursor.execute(statement, [track])
        times_played = cursor.fetchone()
        statement = "UPDATE track SET times_played = ? WHERE id = ?"
        cursor.execute(statement, [times_played + 1, track])
        db.commit()
    return "Played", 200







