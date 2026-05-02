import sqlite3

DB_NAME = "myMemoria.db"

def create_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_table():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            judul TEXT NOT NULL,
            isi_catatan TEXT NOT NULL,
            kategori TEXT NOT NULL,
            mood TEXT NOT NULL
        )
        """)

def insert_entry(tanggal, judul, isi, kategori, mood):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO entries (tanggal, judul, isi_catatan, kategori, mood)
            VALUES (?, ?, ?, ?, ?)
        """, (tanggal, judul, isi, kategori, mood))

def get_all_entries():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM entries
            ORDER BY tanggal DESC
        """)
        return cursor.fetchall()

def search_by_title(keyword):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM entries
            WHERE judul LIKE ?
            ORDER BY tanggal DESC
        """, ('%' + keyword + '%',))
        return cursor.fetchall()

def delete_entry_by_id(entry_id):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM entries WHERE id=?
        """, (entry_id,))

def update_entry(entry_id, tanggal, judul, isi, kategori, mood):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE entries
            SET tanggal=?, judul=?, isi_catatan=?, kategori=?, mood=?
            WHERE id=?
        """, (tanggal, judul, isi, kategori, mood, entry_id))