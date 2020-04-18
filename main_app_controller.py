import tkinter as tk
from player_window import PlayerWindow
from tkinter.filedialog import askopenfilename
import requests
from tkinter import messagebox
from song import Song
from update_song_window import UpdateSongWindow
from add_song_window import AddSongWindow
import eyed3
import os
import vlc
from song_info_window import SongInfoWindow
from queue_window import QueueWindow


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
        self._posn = 0
        self._queue_list = []


    # Windows
    def add_song_popup(self):
        """ Shows entry field popup"""
        self._add_win = tk.Toplevel()
        self._add_song = AddSongWindow(self._add_win,
                                             self._close_add_song_popup,
                                             self.add_callback, self.open_callback)

    def _close_add_song_popup(self):
        """ Close Add popup"""

        self._add_win.destroy()

    def update_song_popup(self):
        """ Shows entry field popup"""
        try:
            song_listbox = self._player.song_listbox
            item = song_listbox.curselection()
            index = item[0]
            song_info = song_listbox.get(index)

            self._update_win = tk.Toplevel()
            self._update_song = UpdateSongWindow(self._update_win,
                                                 self._close_update_song_popup,
                                                 self.update_callback, song_info)
        except:
            messagebox.showinfo(title='Selection failed', message='Please select a song from the list first')


    def _close_update_song_popup(self):
        """ Close Update popup"""

        self._update_win.destroy()

    def song_info_popup(self):
        """ Shows entry field popup"""
        try:
            song_listbox = self._player.song_listbox
            item = song_listbox.curselection()
            index = item[0]
            song_info = song_listbox.get(index)
            data = self.info_callback(song_info)

            self._info_win = tk.Toplevel()
            self._song_stats = SongInfoWindow(self._info_win,
                                                 self._close_song_info_popup,
                                                 song_info, data)

        except:
            messagebox.showinfo(title='Selection failed', message='Please select a song from the list first')


    def _close_song_info_popup(self):
        """ Close Update popup"""
        self._info_win.destroy()

    def queue_window_popup(self):
        """ Shows queue popup"""
        self._queue_win = tk.Toplevel()
        self._queue = QueueWindow(self._queue_win,
                                  self._close_queue_popup,
                                  self.remove_callback,
                                  self._queue_list)

        self._queue.set_songs(self._queue_list)


    def _close_queue_popup(self):
        """ Close Update popup"""
        self._queue_win.destroy()

    # Callbacks

    def add_queue_callback(self):
        """ Adds item to queue """
        song_listbox = self._player.song_listbox
        # queue_listbox = self._queue.queue_listbox

        try:
            index = song_listbox.curselection()
            item = song_listbox.get(index)
            self._queue_list.append(item)

            messagestr = f'Successfully added {item} to the queue'
            messagebox.showinfo(title='Add Successful', message=messagestr)

        except:
            messagestr = 'Please select an item in the song listbox'
            messagebox.showinfo(title='Add failed', message=messagestr)


        return

    def remove_callback(self):
        """ Removes an item from the queue list in the queue window"""

        try:
            item = self._queue.queue_listbox.curselection()
            index = item[0]
            self._queue_list.pop(index)
            self._queue.set_songs(self._queue_list)
        except:
            messagebox.showinfo(title='Error', message='Please choose an item in the list')

    def open_callback(self):
        """ Load all the names from the file """
        selected_file = askopenfilename(initialdir='.')
        if selected_file:
            self.file_name = os.path.abspath(selected_file)

            song_data = self.load(self.file_name)

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


    def update_callback(self):
        """ Updates the song value """
        form_data = self._update_song.get_form_data()
        song_info = self._update_song.song_data

        response = requests.put("http://localhost:5000/song/" + song_info, json=form_data)

        if response.status_code == 200:
            msg_str = f'{song_info} updated'
            messagebox.showinfo(title='Update Song', message=msg_str)

        if response.status_code == 400:
            msg_str = 'Song update failed'
            messagebox.showinfo(title='Update Song', message=msg_str)

        self._update_song._close_cb()

        return


    def clear_callback(self):
        """ Remove all students names from system. """
        response = requests.delete("http://localhost:5000/song/all")
        if response.status_code == 200:
            msg_str = f'All songs removed from the database'
            messagebox.showinfo(title='Delete All', message=msg_str)
            self._player._current_song['text'] = ''
            self._player._current_state['text'] = ''
            self._player.song_listbox.delete(0, tk.END)
        else:
            messagebox.showerror(title='Delete All', message="Something went wrong")


    def quit_callback(self):
        """ Exit the application. """
        self.master.quit()


    def add_callback(self):
        """ Add a new student name to the file. """
        form_data = self._add_song.get_form_data()
        song_data = self.load(form_data)

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


    def delete_callback(self):
        """ Deletes a student from the list and db"""
        song_listbox = self._player.song_listbox

        item = song_listbox.curselection()
        try:
            index = item[0]
            song_info = song_listbox.get(index)

            response = requests.delete("http://localhost:5000/song/" + song_info)

            if response.status_code == 200:
                msg_str = f'{song_info} deleted from the database'
                messagebox.showinfo(title='Add Student', message=msg_str)

            self.listbox_callback()

        except:
            messagebox.showinfo(title='Error', message='Please choose an item in the list')


    def listbox_callback(self):
        """ Gets a list of all songs and """
        response_names = requests.get("http://localhost:5000/song/songs")
        song_list = [f'{s["title"]} - {s["artist"]}' for s in response_names.json()]
        song_listbox = self._player.song_listbox
        song_listbox.delete(0, tk.END)
        for song in song_list:
            song_listbox.insert(tk.END, song)


    def info_callback(self, song_info):
        """ Generates value for chosen song"""
        response = requests.get("http://localhost:5000/song/" + song_info)

        return response.json()


    def play_queue_callback(self):
        """ Starts playing songs in the queue"""

        try:
            song_info = self._queue_list[0]
            self.update_helper(song_info)
            title = song_info[0]
            response = requests.get("http://localhost:5000/song/" + song_info)

            # Updates play count and date added

            if self._media_player.get_state() == vlc.State.Playing:
                self._media_player.stop()
            media_file = response.json()['path_name']

            media = self._vlc_instance.media_new_path(media_file)
            self._media_player.set_media(media)
            self._media_player.play()
            self._current_title = title
            self._player._current_song['text'] = song_info
            self._player._current_state['text'] = 'Playing'

            self._posn = 1

        except:
            messagebox.showinfo(title='Queue empty',
                                message=f'Please add songs to queue before trying to play')

        return


    def play_next_callback(self):
        """ Starts playing songs in the queue"""

        try:
            song_info = self._queue_list[self._posn]
            self.update_helper(song_info)
            title = song_info[0]
            response = requests.get("http://localhost:5000/song/" + song_info)

            # Updates play count and date added

            if self._media_player.get_state() == vlc.State.Playing:
                self._media_player.stop()
            media_file = response.json()['path_name']

            media = self._vlc_instance.media_new_path(media_file)
            self._media_player.set_media(media)
            self._media_player.play()
            self._current_title = title
            self._player._current_song['text'] = song_info
            self._player._current_state['text'] = 'Playing'

            self._posn += 1

        except:
            messagebox.showinfo(title='Queue finished',
                                message=f'You\'ve reached the end of your queue')

        return


    def play_callback(self):
        """Play a song specified by number. """
        song_listbox = self._player.song_listbox
        item = song_listbox.curselection()
        try:
            index = item[0]
            song_info = song_listbox.get(index)

            # At the moment doesn't work
            self.update_helper(song_info)

            title = song_info[0]
            if title is None:
                messagebox.showinfo(title="Invalid Choice",
                        message=f"Invalid song, please us the listbox to select a song from the"\
                                f"listbox.")
                return

            response = requests.get("http://localhost:5000/song/" + song_info)

            # Updates play count and date added

            if self._media_player.get_state() == vlc.State.Playing:
                self._media_player.stop()
            media_file = response.json()['path_name']

            media = self._vlc_instance.media_new_path(media_file)
            self._media_player.set_media(media)
            self._media_player.play()
            self._current_title = title
            self._player._current_song['text'] = song_info
            self._player._current_state['text'] = 'Playing'
        except:
            messagebox.showinfo(title='Error', message='Please choose an item in the list')

        return


    def update_helper(self, song_info):
        """ Updates play count and date added """

        response = requests.put("http://localhost:5000/song/usage/" + song_info)

        if response.status_code == 200:
            msg_str = f'{song_info} updated'


        if response.status_code == 400:
            msg_str = 'Song update failed'

        return


    def pause_callback(self):
        """ Pause the player """
        if self._media_player.get_state() == vlc.State.Playing:
            self._media_player.pause()
        self._player._current_state['text'] = 'Paused'


    def resume_callback(self):
        """ Resume playing """
        if self._media_player.get_state() == vlc.State.Paused:
            self._media_player.pause()
        self._player._current_state['text'] = 'Playing'


    def stop_callback(self):
        """ Stop the player """
        self._media_player.stop()
        self._player._current_state['text'] = ''
        self._player._current_song['text'] = ''


    def load(self, song_url):
        """ Loads a song by the url"""

        mp3_file = eyed3.load(song_url)


        runtime = mp3_file.info.time_secs
        mins = int(runtime // 60)
        secs = int(runtime % 60)
        runtime = ('{}:{}'.format(mins, secs))

        song_info = { "title": getattr(mp3_file.tag, 'title'),
            "artist": getattr(mp3_file.tag, 'artist'),
            "runtime": runtime,
            "path_name": song_url,
            "album": getattr(mp3_file.tag, 'album'),
            "genre": str(getattr(mp3_file.tag, 'genre'))
                    }

        return song_info


if __name__ == "__main__":
 """ Create Tk window manager and a main window. Start the main loop """
 root = tk.Tk()
 MainAppController(root).pack()
 tk.mainloop()