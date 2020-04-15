from typing import Dict, List
from audio_file import AudioFile
from sqlalchemy import Column, Text

class Song(AudioFile):
    """ Represents an abstract song, this is a subclass of the
        AudioFile class

    Name: Roy Ortega
    Set: 2B
    Date: January 31, 2020
    """

    """ ORM: map db columns to instance variables in this class """
    album = Column(Text)
    genre = Column(Text)

    def __init__(self, title: str, artist: str, runtime: str, path_name: str, album: str = None, genre: str = None):
        """Creates an object instance of the song subclass"""
        super().__init__(title, artist, runtime, path_name)
        self.album = album
        self.genre = genre
        self.__validate_song(album, genre)

    @staticmethod
    def __validate_song(album, genre):
        """Validates the song specific arguments"""
        if album is not None and (type(album) != str):
            raise ValueError('Album must either not be included or a string')
        elif genre is not None and (type(genre) != str):
            raise ValueError('Genre must either not be included or a string')
        else:
            return True

    def get_description(self) -> str:
        """Returns a string that includes the relevant song information"""
        song_info = "{} by {} from the album {} added on {}. Runtime is {}. Last played on {}."\
            .format(self.title, self.artist, self.album, self.date_added,
                    self.runtime, self.last_played)

        if self._genre is not None:
            genre_string = ''
            for i in self._genre:
                genre_string += ('"' + i + '"' + ', ')
            genre_string = genre_string.strip(', ')
            song_info += ' The song fits in the following genre(s) {}.'.format(genre_string)

        if self.rating is not None:
            song_info += " User rating is {}/5".format(self.rating)

        return song_info


    def meta_data(self) -> Dict:
        """Creates meta data for this specific song instance in the form of a dictionary"""
        self._song_dict = {}
        self._song_dict.update([('title', self.title), ('artist', self.artist), ('album', self.album),
                                ('date_added', self.date_added), ('runtime', self.runtime),
                                ('last_played', self.last_played), ('rating', self.rating),
                                ('genre', self.genre)])
        return self._song_dict

    def update(self, new_data: object):
        """ Copy all changes fields into the actual object (self). """
        if not isinstance(new_data, Song):
            raise TypeError("new_data must be a Song object")
        if new_data.id != self.id:
            raise ValueError("Song ID cannot be changed")
        if new_data.rating != None:
            self.rating = new_data.rating
        if new_data.genre != None:
            self.genre = new_data.genre
        if new_data.album != None:
            self.album = new_data.album