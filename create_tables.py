import sqlite3

conn = sqlite3.connect('song_db.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE song_tbl
          (title TEXT PRIMARY KEY,
           artist TEXT NOT NULL,
           runtime TEXT NOT NULL,
           path_name TEXT NOT NULL,
           album TEXT NOT NULL,
           genre TEXT)
          ''')

conn.commit()
conn.close()
