from db import get_db
from base64 import b64encode

def get_artists():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id, name, age, albums, tracks, self FROM artist"
    cursor.execute(query)
    return cursor.fetchall()

def get_by_id(id_artist):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, name, age, albums, tracks, self FROM artist WHERE id = ?"
    cursor.execute(statement, [id_artist])
    return cursor.fetchone(), 200

def get_artists_albums_by_id(id_artist):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, artist_id, name, genre, artist, tracks, self FROM album WHERE artist_id = ?"
    cursor.execute(statement, [id_artist])
    return cursor.fetchone(), 200

def get_artists_tracks_by_id(id_artist):
    db = get_db()
    cursor = db.cursor()
    tracks = []
    statement = "SELECT id FROM album WHERE id_artist = ?"
    cursor.execute(statement, [id_artist])
    db.commit()
    albums = cursor.fetchall()
    for album in albums:
        statement = "SELECT id, album_id, name, duration, times_played, artist, album, self FROM track WHERE id_album = ?"
        cursor.execute(statement, [album])
        db.commit()
        track_album = cursor.fetchall()
        tracks.append(track_album)
    return tracks, 200


def insert_artist(name, age):
    db = get_db()
    cursor = db.cursor()
    id_artist = b64encode(name.encode()).decode('utf-8')
    if len(id_artist) >= 22:
        id_artist = id_artist[:22]
    statement = "INSERT INTO artist(id, name, age, albums, tracks, self) VALUES (?, ?, ?, ?, ?, ?)"
    albums = f"https://t2-tdi.herokuapp.com/artists/{id_artist}/albums"
    tracks = f"https://t2-tdi.herokuapp.com/artists/{id_artist}/tracks"
    self_page = f"https://t2-tdi.herokuapp.com/artists/{id_artist}"
    cursor.execute(statement, [id_artist, name, age, albums, tracks, self_page])
    db.commit()
    return True

def delete_artist(id_artist):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM artist WHERE id = ?"
    cursor.execute(statement, [id_artist])
    db.commit()
    return "Artista borrado", 204

def play_tracks(id_artist):
    db = get_db()
    cursor = db.cursor()
    tracks = []
    statement = "SELECT id FROM album WHERE id_artist = ?"
    cursor.execute(statement, [id_artist])
    db.commit()
    albums = cursor.fetchall()
    for album in albums:
        statement = "SELECT id FROM track WHERE id_album = ?"
        cursor.execute(statement, [album])
        db.commit()
        track_album = cursor.fetchall()
        tracks.append(track_album)
    for track in tracks:
        statement = "SELECT times_played FROM track WHERE id = ?"
        cursor.execute(statement, [track])
        db.commit()
        times_played = cursor.fetchone()
        statement = "UPDATE track SET times_played = ? WHERE id = ?"
        cursor.execute(statement, [times_played + 1, track])
        db.commit()
    return True
