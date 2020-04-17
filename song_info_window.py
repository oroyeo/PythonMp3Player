import tkinter as tk


class SongInfoWindow(tk.Frame):

    def __init__(self, parent, close_callback, song_info, data):
        """ Initialize the popup update song window """
        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.song_data = song_info

        parent.title('Song info')

        # Frames
        self.top_frame = tk.Frame(master=parent)
        self.top_frame.grid(row=0, padx=30, pady=10)
        self.mid_frame = tk.Frame(master=parent)
        self.mid_frame.grid(row=1, column=0, padx=30, pady=10)
        self.entry_frame = tk.Frame(master=parent)
        self.entry_frame.grid(row=1, column=1, padx=30, pady=10)
        self.bot_frame = tk.Frame(master=parent)
        self.bot_frame.grid(row=2, padx=30, pady=10)

        # Labels
        tk.Label(self.top_frame, text='Song:').grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self._song_name = tk.Label(self.top_frame, text=self.song_data)
        self._song_name.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        tk.Label(self.mid_frame, text='Title:').grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Label(self.mid_frame, text='Artist:').grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Label(self.mid_frame, text='Album:').grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Label(self.mid_frame, text='Genre:').grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Label(self.mid_frame, text='Rating:').grid(row=4, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Label(self.mid_frame, text='Date Added:').grid(row=5, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Label(self.mid_frame, text='Last Played:').grid(row=6, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Label(self.mid_frame, text='Play Count:').grid(row=7, column=0, sticky=tk.E, padx=5, pady=5)

        tk.Label(self.mid_frame, text=data['title']).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        tk.Label(self.mid_frame, text=data['artist']).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        tk.Label(self.mid_frame, text=data['album']).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        tk.Label(self.mid_frame, text=data['genre']).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        tk.Label(self.mid_frame, text=data['rating']).grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        tk.Label(self.mid_frame, text=data['date_added']).grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        tk.Label(self.mid_frame, text=data['last_played']).grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        tk.Label(self.mid_frame, text=data['play_count']).grid(row=7, column=1, sticky=tk.W, padx=5, pady=5)



        self.close_button = tk.Button(self.bot_frame, text='Close', width=10,
                                   command=self._close_cb)


        self.close_button.pack()

