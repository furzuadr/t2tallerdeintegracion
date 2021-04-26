from db import get_db
from base64 import b64encode

def get_albums():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id, artist_id, name, genre, artist, tracks, self FROM album"
    cursor.execute(query)
    return cursor.fetchall()

def get_by_id(id_album):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, artist_id, name, genre, artist, tracks, self FROM album WHERE id = ?"
    cursor.execute(statement, [id_album])
    return cursor.fetchone(), 200

def get_album_tracks_by_id(id_album):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, album_id, name, duration, times_played, artist, album, self FROM track WHERE id_album = ?"
    cursor.execute(statement, [id_album])
    db.commit()
    return cursor.fetchall(), 200


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
    return 201

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
    db.commit()
    track_album = cursor.fetchall()
    for track in track_album:
        statement = "SELECT times_played FROM track WHERE id = ?"
        cursor.execute(statement, [track])
        db.commit()
        times_played = cursor.fetchone()
        statement = "UPDATE track SET times_played = ? WHERE id = ?"
        cursor.execute(statement, [times_played + 1, track])
        db.commit()
    return True







