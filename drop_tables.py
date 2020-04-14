import sqlite3

conn = sqlite3.connect('song_db.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE song_tbl
          ''')

conn.commit()
conn.close()
