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


class MainAppController(tk.Frame):
    """ Main Application Window """

    def __init__(self, parent):
        """ Create the views """
        tk.Frame.__init__(self, parent)
        self._root_win = tk.Toplevel()
        self._player = PlayerWindow(self._root_win, self)

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

    """ Don't need this """
    # def rand_callback(self):
    #  """ Random select a name and display on GUI. """
    #  response = requests.get("http://localhost:5000/student/random")
    #  student = Student.from_dict(response.json())
    #  if response.status_code == 200:
    #     full_name = f"{student.first_name} {student.last_name}"
    #     self._chooser.display_student_name(full_name)
    #  elif response.status_code == 404:
    #     messagebox.showinfo(title='Random', message="No names in DB")

    def add_callback(self):
        """ Add a new student name to the file. """
        form_data = self._add_song.get_form_data()
        print(len(form_data))
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
        # response_names = requests.get("http://localhost:5000/student/names")
        # name_list = [f'{s["first_name"]} {s["last_name"]}' for s in response_names.json()]
        # self._class.set_names(name_list)
        self._add_song._close_cb()
        return

    """ Don't need this? Unless we refactor it to make it open file on click """
    # def openfile(self):
    #     """ Load all the names from the file """
    #     selected_file = askopenfilename(initialdir='.')
    #     if selected_file:
    #         self.file_name = selected_file
    #         num_added = 0
    #         not_added = []
    #         with open(self.file_name, 'r') as csvfile:
    #             csv_reader = csv.reader(csvfile, delimiter=',')
    #             for row in csv_reader:
    #                 data = {'student_id': row[0],
    #                         'first_name': row[1],
    #                         'last_name': row[2]}
    #                 response = requests.post("http://localhost:5000/student",
    #                              json=data)
    #                 if response.status_code == 200:
    #                     num_added += 1
    #                 else:
    #                     not_added.append(' '.join(row))
    #         msg = f'{num_added} names added to DB.'
    #         if len(not_added) > 0:
    #             not_added = '\n'.join(not_added)
    #             msg += '\n' + f'The following names were not added:'
    #             msg += '\n' + not_added
    #         messagebox.showinfo(title='Load Names', message=msg)


    def classlist_popup(self):
        """ Show Classlist Popup Window """
        self._class_win = tk.Toplevel()
        self._class = ClasslistWindow(self._class_win, self._close_classlist_popup, self.delete_callback, self)
        response = requests.get("http://localhost:5000/student/names")

        name_list = [f'{s["first_name"]} {s["last_name"]}' for s in response.json()]
        self._class.set_names(name_list)


    def _close_classlist_popup(self):
        """ Close Classlist Popup """

        self._class_win.destroy()


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
        student_listbox = self._class.name_listbox
        item = student_listbox.curselection()
        index = item[0]

        student_name = self._class.name_listbox.get(index)

        response = requests.delete("http://localhost:5000/student/" + student_name)

        if response.status_code == 200:
            msg_str = f'{student_name} deleted from the database'
            messagebox.showinfo(title='Add Student', message=msg_str)

        response_names = requests.get("http://localhost:5000/student/names")
        name_list = [f'{s["first_name"]} {s["last_name"]}' for s in response_names.json()]
        self._class.set_names(name_list)

    """ Use this to start the add song """
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