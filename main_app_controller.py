import tkinter as tk
from player_window import PlayerWindow
from tkinter.filedialog import askopenfilename
import requests
from tkinter import messagebox
from song import Song
from classlist_window import ClasslistWindow
from add_song_window import AddSongWindow
import eyed3
import os
import vlc


class MainAppController(tk.Frame):
    """ Main Application Window """

    def __init__(self, parent):
        """ Create the views """
        tk.Frame.__init__(self, parent)
        self._root_win = tk.Toplevel()
        self._player = PlayerWindow(self._root_win, self)
        self.listbox_callback()

        self._vlc_instance = vlc.Instance()
        self._media_player = self._vlc_instance.media_player_new()

    # 6: define callback functions
    def clear_callback(self):
        """ Remove all students names from system. """
        response = requests.delete("http://localhost:5000/song/all")
        if response.status_code == 200:
            msg_str = f'All songs removed from the database'
            messagebox.showinfo(title='Delete All', message=msg_str)
        else:
            messagebox.showerror(title='Delete All', message="Something went wrong")

    def quit_callback(self):
        """ Exit the application. """
        self.master.quit()

    def add_callback(self):
        """ Add a new student name to the file. """
        form_data = self._add_song.get_form_data()
        song_data = self.load(form_data)

        if len(form_data) != 1:
            messagebox.showerror(title='Invalid url data',
                                 message='Enter "Song URL')
            return

        response = requests.post("http://localhost:5000/song", json=song_data)
        if response.status_code == 200:
            msg_str = f'{song_data["title"]}, {song_data["artist"]}' \
                      f' added to the database'
            messagebox.showinfo(title='Add Song', message=msg_str)

        if response.status_code == 400:
            msg_str = 'Song already exists'
            messagebox.showinfo(title='Add Song', message=msg_str)

        self.listbox_callback()
        self._add_song._close_cb()
        return


    def add_song_popup(self):
        """ Shows entry field popup"""
        self._add_win = tk.Toplevel()
        self._add_song = AddSongWindow(self._add_win,
                                             self._close_add_song_popup,
                                             self.add_callback)

    def _close_add_song_popup(self):
        """ Close Add popup"""

        self._add_win.destroy()

    def delete_callback(self):
        """ Deletes a student from the list and db"""
        song_listbox = self._player.song_listbox
        item = song_listbox.curselection()
        index = item[0]
        song_info = song_listbox.get(index)

        response = requests.delete("http://localhost:5000/song/" + song_info)

        if response.status_code == 200:
            msg_str = f'{song_info} deleted from the database'
            messagebox.showinfo(title='Add Student', message=msg_str)

        self.listbox_callback()

    def listbox_callback(self):
        """ Gets a list of all songs and """
        response_names = requests.get("http://localhost:5000/song/songs")
        song_list = [f'{s["title"]} - {s["artist"]}' for s in response_names.json()]
        song_listbox = self._player.song_listbox
        song_listbox.delete(0, tk.END)
        for song in song_list:
            song_listbox.insert(tk.END, song)


    def play_callback(self):
        """Play a song specified by number. """
        song_listbox = self._player.song_listbox
        item = song_listbox.curselection()
        index = item[0]
        song_info = song_listbox.get(index)

        title = song_info[0]
        if title is None:
            messagebox.showinfo(title="Invalid Choice",
                    message=f"Invalid song, please us the listbox to select a song from the"\
                            f"listbox.")
            return

        response = requests.get("http://localhost:5000/song/" + song_info)

        if self._media_player.get_state() == vlc.State.Playing:
            self._media_player.stop()
        media_file = response.json()['path_name']
        media = self._vlc_instance.media_new_path(media_file)
        self._media_player.set_media(media)
        self._media_player.play()
        self._current_title = title
        print(f"Playing {title} from file {media_file}")

    def pause_callback(self):
        """ Pause the player """
        if self._media_player.get_state() == vlc.State.Playing:
            self._media_player.pause()
        print(f"Player paused during playback of {self._current_title}")

    def resume_callback(self):
        """ Resume playing """
        if self._media_player.get_state() == vlc.State.Paused:
            self._media_player.pause()
        print(f"Playback of {self._current_title} resumed")

    def load(self, song_url):
        """ Loads a song by the url"""
        split_path = os.path.split(song_url['path_name'])
        mp3_path = split_path[0]
        mp3_file = eyed3.load(song_url['path_name'])
        runtime = mp3_file.info.time_secs
        mins = int(runtime // 60)
        secs = int(runtime % 60)
        runtime = ('{}:{}'.format(mins, secs))

        song_info = { "title": getattr(mp3_file.tag, 'title'),
            "artist": getattr(mp3_file.tag, 'artist'),
            "runtime": runtime,
            "path_name": song_url['path_name'],
            "album": getattr(mp3_file.tag, 'album'),
            "genre": str(getattr(mp3_file.tag, 'genre'))
                    }

        return song_info




if __name__ == "__main__":
 """ Create Tk window manager and a main window. Start the main loop """
 root = tk.Tk()
 MainAppController(root).pack()
 tk.mainloop()