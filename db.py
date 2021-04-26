import sqlite3


def get_db():
    conn = sqlite3.connect("api.db")
    return conn


def create_tables():
    tables = ["""CREATE TABLE IF NOT EXISTS artist(
                id TEXT PRIMARY KEY,
                name TEXT,
				age INTEGER,
				albums TEXT,
                tracks TEXT,
                self TEXT
                )""",
                """CREATE TABLE IF NOT EXISTS album(
                id TEXT PRIMARY KEY,
                artist_id TEXT,
				name TEXT,
				genre TEXT,
                artist TEXT,
                tracks TEXT,
                self TEXT,
                FOREIGN KEY(artist_id) REFERENCES artist(id) ON DELETE CASCADE
                )""",
                """CREATE TABLE IF NOT EXISTS track(
                id TEXT PRIMARY KEY,
                album_id TEXT,
				name TEXT,
				duration FLOAT,
                times_played INTEGER,
                artist TEXT,
                album TEXT,
                self TEXT,
                FOREIGN KEY(album_id) REFERENCES album(id) ON DELETE CASCADE
                )"""
            
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)