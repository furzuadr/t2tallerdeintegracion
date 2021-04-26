from db import get_db
from base64 import b64encode
from album import check_album

def get_tracks():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id, album_id, name, duration, times_played, artist, album, self FROM track"
    cursor.execute(query)
    tracks = cursor.fetchall()
    for a in tracks:
        tracks_lista.append({"id": a[0], "album_id": a[1], "name": a[2], "duration": a[3], "times_played": a[4], "artist": a[5], "album": a[6], "self": a[7]})
    return tracks_lista, 200

def get_by_id(id_track):
    flag_existe, dict_track = check_track(id_track, True)
    if not flag_existe:
        return "No existe", 404

    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, album_id, name, duration, times_played, artist, album, self FROM track WHERE id = ?"
    cursor.execute(statement, [id_track])
    track = cursor.fetchone()
    tracks_lista = {"id": track[0], "album_id": track[1], "name": track[2], "duration": track[3], "times_played": track[4], "artist": track[5], "album": track[6], "self": track[7]}
    return tracks_lista, 200 

def insert_track(id_album, name, duration):
    if flag_input:
        return "Input invalido", 400
    flag_album, dict_album = check_album(id_album, True)
    if not flag_album:
        return "No existe album", 422
    flag_input = check_input(name, duration)
    flag_existe, dict_track = check_exists(name, False)
    if flag_existe:
        return dict_track, 409


    db = get_db()
    cursor = db.cursor()
    id_track = b64encode(name.encode()).decode('utf-8')
    if len(id_track) >= 22:
        id_track = id_track[:22]
    statement = "SELECT artist_id FROM album WHERE id_album = ?"
    cursor.execute(statement, [id_album])
    id_artist = cursor.fetchone()
    statement = "INSERT INTO track(id, album_id, name, duration, times_played, artist, album, self) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    artist = f"https://t2-tdi.herokuapp.com/artists/{id_artist}"
    album = f"https://t2-tdi.herokuapp.com/albums/{id_album}"
    self_page = f"https://t2-tdi.herokuapp.com/tracks/{id_album}"
    cursor.execute(statement, [id_track, id_album, name, duration, 0, artist, album, self_page])
    db.commit()
    return {"id": id_track, "album_id": id_album, "name": name, "duration": duration, "times_played": 0, "artist": artist, "album": album, "self": self_page}, 201

def delete_track(id_track):
    flag_existe, dict_track = check_track(id_track, True)
    if not flag_existe:
        return "No existe", 404

    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM track WHERE id = ?"
    cursor.execute(statement, [id_track])
    db.commit()
    return "Track borrado", 204

def play_tracks(id_track):
    flag_existe, dict_track = check_track(id_track, True)
    if not flag_existe:
        return "No existe", 404

    db = get_db()
    cursor = db.cursor()
    statement = "SELECT times_played FROM track WHERE id = ?"
    cursor.execute(statement, [id_track])
    times_played = cursor.fetchone()
    statement = "UPDATE track SET times_played = ? WHERE id = ?"
    cursor.execute(statement, [times_played + 1, id_track])
    db.commit()
    return "Played", 200

def check_input(name, duration):
    if type(name) != str or type(duration) != float:
        return True
    else:
        return False

def check_exists(name, flag):
    if flag:
        id_track = name
    else:
        id_track = b64encode(name.encode()).decode('utf-8')
        if len(id_track) >= 22:
            id_track = id_track[:22]
    id_track = b64encode(name.encode()).decode('utf-8')
    if len(id_track) >= 22:
        id_track = id_track[:22]
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, album_id, name, duration, times_played, artist, album, self FROM track WHERE id = ?"
    cursor.execute(statement, [id_track])
    track = cursor.fetchone()
    if album:
        return True, {"id": track[0], "album_id": track[1], "name": track[2], "duration": track[3], "times_played": track[4], "artist": track[5], "album": track[6], "self": track[7]}
    else:
        return False, 0







