from datetime import datetime
import os
from typing import Dict
from abc import abstractmethod
from base import Base
from sqlalchemy import Column, Text, Integer

class AudioFile(Base):
    """ Represents an abstract AudioFile

    Name: Roy Ortega, Nathan Broyles, Adrian Chan
    Set: 2B
    Date: April 14, 2020
    """

    _DATE_FORMAT = "%Y-%m-%d"

    __tablename__ = "song_tbl"
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    artist = Column(Text, nullable=False)
    runtime = Column(Text)
    path_name = Column(Text, nullable=False)
    file_path = Column(Text)
    file_name = Column(Text)
    date_added = Column(Text, nullable=False)
    play_count = Column(Integer, nullable=False)
    last_played = Column(Text)
    rating = Column(Integer)

    def __init__(self, title: str, artist: str, runtime: str, path_name: str):
        """Creates an object instance of the audio_file class"""
        self.title = title
        self.artist = artist
        self.runtime = runtime
        self.rating = None
        self.path_name = path_name
        self.file_path = None
        self.file_name = None
        self.date_added = datetime.now().strftime(AudioFile._DATE_FORMAT)
        self.play_count = 0
        self.last_played = None
        self.__set_file_info(path_name)
        self.__validate_info(title, artist, runtime, path_name)
        self.__validate_location()
        self.__validate_class(self)



    @staticmethod
    def __validate_info(title: str, artist: str, runtime: str, path_name: str):
        """Validates whether each argument is the proper type"""
        if (type(title) != str) or (type(artist) != str) or (type(runtime) != str) \
                or (type(path_name) != str):
            raise ValueError


    @staticmethod
    def __validate_class(self):
        """Validates that the class is not an audio file"""
        if type(self) == AudioFile:
            raise ValueError('Cannot be the base-type AudioFile. Must be a song or podcast')


    @property
    def get_title(self) -> str:
        """Returns the title of the current audio_file instance"""
        return self.title


    @property
    def get_artist(self) -> str:
        """Gets the artist for the specific song instance"""
        return self.artist

    @property
    def get_runtime(self) -> str:
        """Returns the runtime for the audio instance"""
        return self.runtime

    @property
    def get_rating(self) -> int:
        """Returns the current user rating for the audio_file instance"""
        return self.rating

    @get_rating.setter
    def get_rating(self, rating: int):
        """Sets the audio_file instance's rating to the entered argument"""
        if type(rating) == int:
            self.rating = rating
        if type(rating) != int:
            raise ValueError
        if rating < 0 or rating > 5:
            print('Rating is out of 5. Please enter an integer from 0 to 5.')
            self.rating = None


    def display_play_count(self):
        """Returns a formatted string that shows the audio_file name and times played"""
        play_string = "{} has been played {} time".format(self.title, self.play_count)

        if self.play_count > 1 or self.play_count == 0:
            play_string += 's'

        print(play_string)


    def __set_file_info(self, path_name):
        """Adds values to the instance variables of _file_path and _file_name"""
        file_name = os.path.basename(path_name)
        file_path = os.path.dirname(path_name)
        self.file_path = file_path
        self.file_name = file_name


    def __validate_location(self):
        """Validates the file location on audio_file creation"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError("Directory does not exist")
        if not os.path.isfile(self.path_name):
            raise FileNotFoundError('File does not exist')


    def file_location(self) -> str:
        """Gets the file path of the audio_file instance"""
        if os.path.exists(self.file_path):
            return "The file ({}) is located in the path ({})".format(self.file_name, self.file_path)
        else:
            raise FileNotFoundError


    @abstractmethod
    def get_description(self) -> str:
        """Abstract method to get the description of the audio file for a subclass"""
        pass

    def update_usage_stats(self):
        """Updates the usage stats for this audio_file instance"""
        self.increment_usage_stats()


    def get_location(self) -> str:
        """Gets file path of audio_file"""
        if os.path.exists(self.path_name):
            return self.path_name
        else:
            raise ValueError("Path does not exist")


    """Code retrieved from usage_stats.py"""

    @property
    def get_date_added(self):
        """ return the date the song or playlist was added to the library """
        return self.date_added.strftime(AudioFile._DATE_FORMAT)

    @property
    def get_last_played(self):
        """ return the date the song or playlist was last played """
        if self.last_played is None:
            return None
        else:
            return self.last_played.strftime(AudioFile._DATE_FORMAT)


    @property
    def get_play_count(self):
        """ return the number of times the song or playlist has been played """
        return self.play_count


    def increment_usage_stats(self):
        """ update the play count and last played time when a song is played """
        self.play_count += 1
        self.last_played = datetime.now()


    @classmethod
    def __valid_datetime(cls, date):
        """ private method to validate the date is datetime object """
        if type(date) is not datetime:
            return False
        else:
            return True

    """ End of usage stats code"""

    @abstractmethod
    def meta_data(self) -> Dict:
        """Abstract method for a dictionary creation to be used by subclasses"""
        pass





