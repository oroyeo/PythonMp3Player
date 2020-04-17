import tkinter as tk


class UpdateSongWindow(tk.Frame):

    def __init__(self, parent, close_callback, update_callback, song_info):
        """ Initialize the popup update song window """
        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self._update_cb = update_callback
        self.song_data = song_info
        parent.title('Update Song')

        # Frames
        self.top_frame = tk.Frame(master=parent)
        self.top_frame.grid(row=0, padx=10, pady=10)
        self.mid_frame = tk.Frame(master=parent)
        self.mid_frame.grid(row=1, column=0, padx=10, pady=10)
        self.entry_frame = tk.Frame(master=parent)
        self.entry_frame.grid(row=1, column=1, padx=10, pady=10)
        self.bot_frame = tk.Frame(master=parent)
        self.bot_frame.grid(row=2, padx=30, pady=10)

        # Labels
        tk.Label(self.top_frame, text='Updating:').grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self._song_name = tk.Label(self.top_frame, text=self.song_data)
        self._song_name.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        tk.Label(self.mid_frame, text='Rating (Out of 5):').grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Label(self.mid_frame, text='Album:').grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Label(self.mid_frame, text='Genre:').grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)

        # Text Entries
        self._rating = tk.Entry(self.mid_frame, width=50)
        self._rating.grid(row=0, column=1, sticky=tk.E)

        self._album = tk.Entry(self.mid_frame, width=50)
        self._album.grid(row=1, column=1, sticky=tk.E)

        self._genre = tk.Entry(self.mid_frame, width=50)
        self._genre.grid(row=2, column=1, sticky=tk.E)

        self.update_song_button = tk.Button(self.bot_frame, text="Update", width=10,
                                    command=self._update_cb)


        self.close_button = tk.Button(self.bot_frame, text='Cancel', width=10,
                                   command=self._close_cb)

        self.update_song_button.pack()
        self.close_button.pack()

    def get_form_data(self):
        """ Return a dictionary of form field values for this form """
        try:
            song_data = {"rating": int(self._rating.get()),
                         "album": self._album.get(),
                         "genre": self._genre.get()}

        except:
            song_data = {"rating": self._rating.get(),
                         "album": self._album.get(),
                         "genre": self._genre.get()}

        return song_data

