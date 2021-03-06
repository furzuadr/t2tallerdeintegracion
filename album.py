from db import get_db
from base64 import b64encode
from artist import check_artist

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
    flag_existe, dict_album = check_album(id_album, False, True)
    if not flag_existe:
        return "No existe", 404

    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, artist_id, name, genre, artist, tracks, self FROM album WHERE id = ?"
    cursor.execute(statement, [id_album])
    album = cursor.fetchone()
    albums_lista = {"id": album[0], "artist_id": album[1], "name": album[2], "genre": album[3], "artist": album[4], "tracks": album[5], "self": album[6]}
    return albums_lista, 200 

def get_album_tracks_by_id(id_album):
    flag_existe, dict_album = check_album(id_album, False, True)
    if not flag_existe:
        return "No existe", 404

    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, album_id, name, duration, times_played, artist, album, self FROM track WHERE album_id = ?"
    cursor.execute(statement, [id_album])
    tracks = cursor.fetchall()
    tracks_lista = []
    for a in tracks:
        a = a[0]
        tracks_lista.append({"id": a[0], "album_id": a[1], "name": a[2], "duration": a[3], "times_played": a[4], "artist": a[5], "album": a[6], "self": a[7]})
    return tracks_lista, 200


def insert_album(id_artist, name, genre):
    flag_input = check_input(name, genre)
    if flag_input:
        return "Input invalido", 400
    if len(id_artist) >= 22:
        id_artist = id_artist[:22]
    flag_artist, dict_artist = check_artist(id_artist, True)
    if not flag_artist:
        return "No existe artista", 422
    flag_existe, dict_album = check_album(name, id_artist, False)
    if flag_existe:
        return dict_album, 409


    db = get_db()
    cursor = db.cursor()
    new_name = f"{name}:{id_artist}"
    id_album = b64encode(new_name.encode()).decode('utf-8')
    if len(id_album) >= 22:
        id_album = id_album[:22]
    statement = "INSERT INTO album(id, artist_id, name, genre, artist, tracks, self) VALUES (?, ?, ?, ?, ?, ?, ?)"
    artist = f"https://t2-tdi.herokuapp.com/artists/{id_artist}"
    tracks = f"https://t2-tdi.herokuapp.com/albums/{id_album}/tracks"
    self_page = f"https://t2-tdi.herokuapp.com/albums/{id_album}"
    cursor.execute(statement, [id_album, id_artist, name, genre, artist, tracks, self_page])
    db.commit()
    return {"id": id_album, "id_artist": id_artist, "name": name, "genre": genre, "artist": artist, "tracks": tracks, "self": self_page}, 201

def delete_album(id_album):
    flag_existe, dict_album = check_album(id_album, False, True)
    if not flag_existe:
        return "No existe", 404

    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM album WHERE id = ?"
    cursor.execute(statement, [id_album])
    db.commit()
    return "Album borrado", 204

def play_tracks(id_album):
    flag_existe, dict_album = check_album(id_album, False, True)
    if not flag_existe:
        print("pasando")
        return "No existe", 404

    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id FROM track WHERE album_id = ?"
    cursor.execute(statement, [id_album])
    track_album = cursor.fetchall()
    for track in track_album:
        track = track[0]
        statement = "SELECT times_played FROM track WHERE id = ?"
        cursor.execute(statement, [track])
        times_played = cursor.fetchone()
        statement = "UPDATE track SET times_played = ? WHERE id = ?"
        cursor.execute(statement, [times_played[0] + 1, track])
        db.commit()
    return "Played", 200

def check_input(name, genre):
    if type(name) != str or type(genre) != str:
        return True
    else:
        return False

def check_album(name, id_artist, flag):
    if flag:
        id_album = name
    else:
        new_name = f"{name}:{id_artist}"
        id_album = b64encode(new_name.encode()).decode('utf-8')
        if len(id_album) >= 22:
            id_album = id_album[:22]
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, artist_id, name, genre, artist, tracks, self FROM album WHERE id = ?"
    cursor.execute(statement, [id_album])
    album = cursor.fetchone()
    if album:
        return True, {"id": album[0], "artist_id": album[1], "name": album[2], "genre": album[3], "artist": album[4], "tracks": album[5], "self": album[6]}
    else:
        return False, 0







