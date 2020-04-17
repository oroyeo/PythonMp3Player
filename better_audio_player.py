from audio_library import AudioLibrary
import vlc



class AudioPlayer:
    """
    This is a better Audio Player (ie: better than the first simple player
    we used. This class consists of a number of commands to instantiate and
    control a vlc instance, as well as a command loop to accept and process
    user commands via a command line interface (cli).

    Once instantiated the player can be controlled by the following commands:
    play list state time pause resume quit stop help
    Each of these commands is implemented in a corresponding method that
    is prefixed with do_, for example do_play, do_help, etc.

    The player is very rudimentary and does not include provisions for
    queueing songs to play, or for playing playlists or podcasts.
    """

    def __init__(self, media_path):
        print("Starting the Audio Player ...")
        self._vlc_instance = vlc.Instance()
        self._player = self._vlc_instance.media_player_new()
        print("Initializing media library ...")
        self._library = AudioLibrary()
        self._library.load(media_path)
        self._current_title = None
        print("\nWelcome to the Audio Player.\n")

    def do_list(self, args):
        """ List all song titles with numbers for playback etc """
        tags = []
        for title in sorted(self._library.titles):
            tags.append(self._library.get_song(title).meta_data())
        col1_width = max([len(tag['title']) for tag in tags])
        col2_width = max([len(tag['artist']) for tag in tags])
        col3_width = max([len(tag['album']) for tag in tags])

        print(f" Num  "
              f"{'Title':{col1_width}}  "
              f"{'Artist':{col2_width}}  "
              f"{'Album':{col3_width}}  "
              f"{'Duration':8}")
        print(f"----  "
              f"{'-' * col1_width:{col1_width}}  "
              f"{'-' * col2_width:{col2_width}}  "
              f"{'-' * col3_width:{col3_width}}  "
              f"{'-' * 8:8}")
        for i, tag in enumerate(tags):
            print(f"{i + 1:3}.  "
                  f"{tag['title']:{col1_width}}  "
                  f"{tag['artist']:{col2_width}}  "
                  f"{tag['album']:{col3_width}}  "
                  f"{tag['runtime']:>6}")

    def do_play(self, num):
        """Play a song specified by number. """
        title = self._get_title_from_num(num)
        if title is None:
            print(f"Invalid song num: {num}. Syntax is: play song_num. Use "
                  f"list to get song_num's.")
            return
        song = self._library.get_song(title)

        if self._player.get_state() == vlc.State.Playing:
            self._player.stop()
        media_file = song.get_location()
        media = self._vlc_instance.media_new_path(media_file)
        self._player.set_media(media)
        self._player.play()
        self._current_title = title
        print(f"Playing {title} from file {media_file}")

    def _get_title_from_num(self, num):
        """ Find the title of a song, given its song number (as displayed
            from list, and as entered by the user).
        """
        try:
            song_num = int(num)
            title = sorted(self._library.titles)[song_num - 1]
        except (IndexError, ValueError, TypeError):
            title = None
        return title

    def do_pause(self, args):
        """ Pause the player """
        if self._player.get_state() == vlc.State.Playing:
            self._player.pause()
        print(f"Player paused during playback of {self._current_title}")

    def do_resume(self, args):
        """ Resume playing """
        if self._player.get_state() == vlc.State.Paused:
            self._player.pause()
        print(f"Playback of {self._current_title} resumed")

    def do_stop(self, args):
        """ Stop the player """
        self._player.stop()
        print(f"Player stopped")

    def do_quit(self, args):
        """ Terminate the program """
        self._player.stop()
        self._player.release()
        print(f"Audio Player exiting.")
        exit(0)

    def do_state(self, args):
        """ Display state of the player. """
        state = str(self._player.get_state()).split('.')[1]
        print(f'Current player state is {state}')
        print(f'Current song: {self._current_title}')
        print(f'Playback posn: {self._get_current_posn()}')

    def do_time(self, args):
        """ Display current play time of current song. """
        if self._current_title is None:
            print("No song playing.")
        else:
            print(f'{self._current_title} {self._get_current_posn()}')

    def _get_current_posn(self):
        """ Return current play time (position in) current song. """
        if self._current_title is None:
            return f"No song playing."
        song = self._library.get_song(self._current_title)
        runtime = song.runtime
        remaining_secs = int(round(self._player.get_time() / 1000, 0))
        mins = int(remaining_secs // 60)
        secs = int(remaining_secs % 60)
        return f"at {mins}:{secs:02d} ... of {runtime}"

    def do_help(self, args):
        """ List names of all methods that can run as commands. """
        methods = [m for m in dir(AudioPlayer) if 'do_' in m]
        cmd_names = "  ".join(methods).replace('do_', '')
        print(f"Commands: " + cmd_names)
