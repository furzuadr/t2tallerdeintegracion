from db import get_db
from base64 import b64encode

def get_tracks():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id, album_id, name, duration, times_played, artist, album, self FROM track"
    cursor.execute(query)
    return cursor.fetchall()

def get_by_id(id_track):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, album_id, name, duration, times_played, artist, album, self FROM track WHERE id = ?"
    cursor.execute(statement, [id_track])
    return cursor.fetchone(), 200

def insert_track(id_album, name, duration):
    db = get_db()
    cursor = db.cursor()
    id_track = b64encode(name.encode()).decode('utf-8')
    if len(id_track) >= 22:
        id_track = id_track[:22]
    statement = "SELECT artist_id FROM album WHERE id_album = ?"
    cursor.execute(statement, [id_album])
    db.commit()
    id_artist = cursor.fetchone()
    statement = "INSERT INTO track(id, album_id, name, duration, times_played, artist, album, self) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    artist = f"https://t2-tdi.herokuapp.com/artists/{id_artist}"
    album = f"https://t2-tdi.herokuapp.com/albums/{id_album}"
    self_page = f"https://t2-tdi.herokuapp.com/tracks/{id_album}"
    cursor.execute(statement, [id_track, id_album, name, duration, 0, artist, album, self_page])
    db.commit()
    return 201

def delete_track(id_track):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM track WHERE id = ?"
    cursor.execute(statement, [id_track])
    db.commit()
    return "Track borrado", 204

def play_tracks(id_track):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT times_played FROM track WHERE id = ?"
    cursor.execute(statement, [id_track])
    db.commit()
    times_played = cursor.fetchone()
    statement = "UPDATE track SET times_played = ? WHERE id = ?"
    cursor.execute(statement, [times_played + 1, id_track])
    db.commit()
    return True







