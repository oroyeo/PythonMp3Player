import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import requests

import os


class PlayerWindow(tk.Frame):
    """ Main Application Window """

    def __init__(self, parent, my_controller):
        """ Initialize Main Application """
        tk.Frame.__init__(self, parent)

        # Window attributes
        parent.title('Audio Player')
        parent.geometry("400x500")

        # Menu - WIP
        main_menu = tk.Menu(master=parent)
        parent.config(menu=main_menu)
        file_menu = tk.Menu(main_menu)
        main_menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Clear', command=my_controller.clear_callback)
        file_menu.add_command(label='Quit', command=my_controller.quit_callback)

        # Frames
        top_frame = tk.Frame(master=parent)
        top_frame.grid(row=0, padx=30, pady=10)
        mid_frame = tk.Frame(master=parent)
        mid_frame.grid(row=1, padx=40, pady=10)

        bot_frame = tk.Frame(master=parent)
        bot_frame.grid(row=2, padx=30, pady=10)

        # Song label
        tk.Label(top_frame, text='Now Playing:').grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self._current_song = tk.Label(top_frame, text='')
        self._current_song.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        tk.Label(top_frame, text='Current State:').grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self._current_state = tk.Label(top_frame, text='')
        self._current_state.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        tk.Label(top_frame, text='Song List').grid(row=2, column=0, sticky=tk.E, padx=5, pady=2)

        # Listbox and scrollbar
        self.song_listbox = tk.Listbox(mid_frame, width=45,
                                       selectmode=tk.BROWSE)
        self.song_scrollbar = tk.Scrollbar(mid_frame, orient='vertical')
        self.song_scrollbar.config(command=self.song_listbox.yview)
        self.song_listbox.config(yscrollcommand=self.song_scrollbar.set)
        self.song_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.song_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons
        tk.Button(bot_frame, text="Play", width=10, command=my_controller.play_callback)\
                .grid(row=0, column=0, sticky=tk.E, padx=20, pady=5)

        tk.Button(bot_frame, text="Pause", width=10, command=my_controller.pause_callback)\
                .grid(row=0, column=1, sticky=tk.E, padx=20, pady=5)

        tk.Button(bot_frame, text="Resume", width=10, command=my_controller.resume_callback)\
                .grid(row=0, column=2, sticky=tk.E, padx=20, pady=5)

        tk.Button(bot_frame, text="Stop", width=10, command=my_controller.stop_callback)\
                .grid(row=1, column=0, sticky=tk.E, padx=20, pady=5)

        tk.Button(bot_frame, text="Add", width=10, command=my_controller.add_song_popup)\
                .grid(row=1, column=1, sticky=tk.E, padx=20, pady=5)

        tk.Button(bot_frame, text="Delete", width=10, command=my_controller.delete_callback)\
                .grid(row=1, column=2, sticky=tk.E, padx=20, pady=5)

        tk.Button(bot_frame, text="Update Song", width=10, command=my_controller.update_song_popup)\
                .grid(row=2, column=0, sticky=tk.E, padx=20, pady=5)

        tk.Button(bot_frame, text="Song Info", width=10, command=my_controller.song_info_popup)\
                .grid(row=3, column=0, sticky=tk.E, padx=20, pady=5)

        tk.Button(bot_frame, text="Queue", width=10, command=self.passer_function())\
                .grid(row=2, column=2, sticky=tk.E, padx=20, pady=5)

        tk.Button(bot_frame, text="View Queue", width=10, command=self.passer_function())\
                .grid(row=3, column=2, sticky=tk.E, padx=20, pady=5)


    def passer_function(self):
        """ Placeholder function"""
        pass