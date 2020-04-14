from datetime import datetime
import os
from typing import Dict
from abc import abstractmethod

class AudioFile:
    """ Represents an abstract AudioFile

    Name: Roy Ortega, Nathan Broyles, Adrian Chan
    Set: 2B
    Date: April 14, 2020
    """

    _DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, title: str, artist: str, runtime: str, path_name: str, date_added: datetime):
        """Creates an object instance of the audio_file class"""
        self._title = title
        self._artist = artist
        self._runtime = runtime
        self._user_rating = None
        self._path_name = path_name
        self._file_path = None
        self._file_name = None
        self.__set_file_info(path_name)
        self.__validate_info(title, artist, runtime, path_name)
        self.__validate_location()
        self.__validate_class(self)
        if self.__valid_datetime(date_added):
            self._date_added = date_added
        else:
            raise ValueError("date_added must be a datetime object")

        self._play_count = 0
        self._last_played = None


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
    def title(self) -> str:
        """Returns the title of the current audio_file instance"""
        return self._title


    @property
    def artist(self) -> str:
        """Gets the artist for the specific song instance"""
        return self._artist

    @property
    def runtime(self) -> str:
        """Returns the runtime for the audio instance"""
        return self._runtime

    @property
    def user_rating(self) -> int:
        """Returns the current user rating for the audio_file instance"""
        return self._user_rating

    @user_rating.setter
    def user_rating(self, rating: int):
        """Sets the audio_file instance's rating to the entered argument"""
        if type(rating) == int:
            self._user_rating = rating
        if type(rating) != int:
            raise ValueError
        if rating < 0 or rating > 5:
            print('Rating is out of 5. Please enter an integer from 0 to 5.')
            self._user_rating = None


    def display_play_count(self):
        """Returns a formatted string that shows the audio_file name and times played"""
        play_string = "{} has been played {} time".format(self._title, self.play_count)

        if self.play_count > 1 or self.play_count == 0:
            play_string += 's'

        print(play_string)


    def __set_file_info(self, path_name):
        """Adds values to the instance variables of _file_path and _file_name"""
        file_name = os.path.basename(path_name)
        file_path = os.path.dirname(path_name)
        self._file_path = file_path
        self._file_name = file_name


    def __validate_location(self):
        """Validates the file location on audio_file creation"""
        if not os.path.exists(self._file_path):
            raise FileNotFoundError("Directory does not exist")
        if not os.path.isfile(self._path_name):
            raise FileNotFoundError('File does not exist')


    def file_location(self) -> str:
        """Gets the file path of the audio_file instance"""
        if os.path.exists(self._file_path):
            return "The file ({}) is located in the path ({})".format(self._file_name, self._file_path)
        else:
            raise FileNotFoundError


    @abstractmethod
    def get_description(self) -> str:
        """Abstract method to get the description of the audio file for a subclass"""
        pass

    def update_usage_stats(self):
        """Updates the usage stats for this audio_file instance"""
        self.increment_usage_stats()


    """ Was this ever used??? """
    # def get_usage_stats(self) -> UsageStats:
    #     """Returns usage stats for the audio_file instance"""
    #     return self._usage

    def get_location(self) -> str:
        """Gets file path of audio_file"""
        if os.path.exists(self._path_name):
            return self._path_name
        else:
            raise ValueError("Path does not exist")


    """Code retrieved from usage_stats.py"""

    @property
    def date_added(self):
        """ return the date the song or playlist was added to the library """
        return self._date_added.strftime(AudioFile._DATE_FORMAT)

    @property
    def last_played(self):
        """ return the date the song or playlist was last played """
        if self._last_played is None:
            return None
        else:
            return self._last_played.strftime(AudioFile._DATE_FORMAT)


    @property
    def play_count(self):
        """ return the number of times the song or playlist has been played """
        return self._play_count


    def increment_usage_stats(self):
        """ update the play count and last played time when a song is played """
        self._play_count += 1
        self._last_played = datetime.now()


    @classmethod
    def __valid_datetime(cls, date):
        """ private method to validate the date is datetime object """
        if type(date) is not datetime:
            return False
        else:
            return True


    @abstractmethod
    def meta_data(self) -> Dict:
        """Abstract method for a dictionary creation to be used by subclasses"""
        pass





