from db import get_db
from base64 import b64encode

def get_artists():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id, name, age, albums, tracks, self FROM artist"
    cursor.execute(query)
    artistas_lista = []
    artistas = cursor.fetchall()
    for a in artistas:
        artistas_lista.append({"id": a[0], "name": a[1], "age": a[2], "albums": a[3], "tracks": a[4], "self": a[5]})
    return artistas_lista, 200 

def get_by_id(id_artist):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, name, age, albums, tracks, self FROM artist WHERE id = ?"
    cursor.execute(statement, [id_artist])
    artista = cursor.fetchone()
    artistas_lista = {"id": artista[0], "name": artista[1], "age": artista[2], "albums": artista[3], "tracks": artista[4], "self": artista[5]}
    return artistas_lista, 200 

def get_artists_albums_by_id(id_artist):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, artist_id, name, genre, artist, tracks, self FROM album WHERE artist_id = ?"
    cursor.execute(statement, [id_artist])
    albums_lista = []
    albums = cursor.fetchall()
    for a in albums:
        albums_lista.append({"id": a[0], "artist_id": a[1], "name": a[2], "genre": a[3], "artist": a[4], "tracks": a[5], "self": a[5]})
    return albums_lista, 200 

def get_artists_tracks_by_id(id_artist):
    db = get_db()
    cursor = db.cursor()
    tracks = []
    statement = "SELECT id FROM album WHERE id_artist = ?"
    cursor.execute(statement, [id_artist])
    albums = cursor.fetchall()
    for album in albums:
        statement = "SELECT id, album_id, name, duration, times_played, artist, album, self FROM track WHERE id_album = ?"
        cursor.execute(statement, [album])
        track_album = cursor.fetchall()
        tracks.append(track_album)
    tracks_lista = []
    tracks = cursor.fetchall()
    for a in tracks:
        tracks_lista.append({"id": a[0], "album_id": a[1], "name": a[2], "duration": a[3], "times_played": a[4], "artist": a[5], "album": a[6], "self": a[7]})
    return tracks_lista, 200 


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
    return {"id": id_artist, "name": name, "age": age, "albums": albums, "tracks": tracks, "self": self_page}, 201

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
    albums = cursor.fetchall()
    for album in albums:
        statement = "SELECT id FROM track WHERE id_album = ?"
        cursor.execute(statement, [album])
        track_album = cursor.fetchall()
        tracks.append(track_album)
    for track in tracks:
        statement = "SELECT times_played FROM track WHERE id = ?"
        cursor.execute(statement, [track])
        times_played = cursor.fetchone()
        statement = "UPDATE track SET times_played = ? WHERE id = ?"
        cursor.execute(statement, [times_played + 1, track])
        db.commit()
    return 200
