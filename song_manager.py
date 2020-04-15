from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base

from song import Song


class SongManager:
    """
    The SongManager class is responsible for coordinating all transactions
    between the higher level programs that use the data, and the actual
    database. Since each transaction is one of the crud operations (create,
    read, update, delete) we provide methods for each of these techniques.

    The class basically just reads and writes data to the database. The
    constructor sets up the initial connection (song object <-> database)
    and each of the other methods performs an autonomous transaction (ie:
    open db session, interact with db, commit changes, close session.
    """

    def __init__(self, song_db):
        """ Creates a Song object and map to the Database """

        if song_db is None or song_db == "":
            raise ValueError(f"Song database [{song_db}] not found")

        engine = create_engine('sqlite:///' + song_db)
        Base.metadata.bind = engine
        self._db_session = sessionmaker(bind=engine)

    def add_song(self, new_song: Song):
        """ Adds a new song to the song database """

        if new_song is None or not isinstance(new_song, Song):
            raise ValueError("Invalid Song Object")

        for song in self.get_all_songs():
            if new_song.title == song.title and new_song.artist == song.artist:
                raise ValueError("Song already exists in the database")

        session = self._db_session()
        session.add(new_song)

        session.commit()

        # song_id = new_song.song_id
        session.close()

        # return song_id

    def update_song(self, song):
        """ Update existing song to match song_upd """
        if song is None or not isinstance(song, Song):
            raise ValueError("Invalid Song Object")

        session = self._db_session()

        existing_song = session.query(Song).filter(
                Song.id == song.id).first()
        if existing_song is None:
            raise ValueError(f"Song {song.id} does not exist")

        existing_song.update(song)

        session.commit()
        session.close()

    def get_song(self, id):
        """ Return song object matching ID"""
        if id is None or type(id) != str:
            raise ValueError("Invalid Song ID")

        session = self._db_session()

        song = session.query(Song).filter(
                Song.id == id).first()

        session.close()

        return song

    def delete_song(self, id):
        """ Delete a song from the database """
        if id is None or type(id) != str:
            raise ValueError("Invalid Song id")

        # song_split = song_name.split()
        # title = song_split[0]
        # artist = song_split[1]

        session = self._db_session()

        song = session.query(Song).filter(
            (Song.id == id)).first()
        if song is None:
            session.close()
            raise ValueError("Song does not exist")

        session.delete(song)
        session.commit()

        session.close()

    def get_all_songs(self):
        """ Return a list of all songs in the DB """
        session = self._db_session()

        all_songs = session.query(Song).all()

        session.close()

        return all_songs

    def delete_all_songs(self):
     """ Delete all songs from the database """
     session = self._db_session()

     session.query(Song).delete()
     session.commit()

     session.close()