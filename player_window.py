import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

import os


class PlayerWindow(tk.Frame):
    """ Main Application Window """

    def __init__(self, parent, my_controller):
        """ Initialize Main Application """
        tk.Frame.__init__(self, parent)

        # 1: create any instances of other support classes that are needed


        # 2: set main window attributes such as title, geometry etc
        parent.title('Audio Player')
        parent.geometry("400x400")

        # 3: set up menus if there are any
        main_menu = tk.Menu(master=parent)
        parent.config(menu=main_menu)
        file_menu = tk.Menu(main_menu)
        main_menu.add_cascade(label='File', menu=file_menu)

        file_menu.add_command(label='Clear', command=my_controller.clear_callback)
        file_menu.add_command(label='Quit', command=my_controller.quit_callback)

        # 4: define frames and place them in the window
        top_frame = tk.Frame(master=parent)
        top_frame.grid(row=0, padx=30, pady=10)
        mid_frame = tk.Frame(master=parent)
        mid_frame.grid(row=1, padx=40, pady=10)
        bot_frame = tk.Frame(master=parent)
        bot_frame.grid(row=2, padx=30, pady=10)


        tk.Label(top_frame, text='File:').grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self._file_value = tk.Label(top_frame, text='Instructions did not say to do anything with this label')
        # self._file_value.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        # tk.Label(mid_frame, text='Random name:').grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)

        # self._name_value = tk.Label(mid_frame, text='')
        # self._name_value.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        self.song_listbox = tk.Listbox(mid_frame, width=45,
                                       selectmode=tk.BROWSE)
        self.song_scrollbar = tk.Scrollbar(mid_frame, orient='vertical')
        self.song_scrollbar.config(command=self.song_listbox.yview)
        self.song_listbox.config(yscrollcommand=self.song_scrollbar.set)
        self.song_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.song_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        
        tk.Button(bot_frame, text="Play", width=10, command=self.passer_function())\
                .grid(row=0, column=0, sticky=tk.E, padx=20, pady=5)

        tk.Button(bot_frame, text="Pause", width=10, command=self.passer_function())\
                .grid(row=0, column=1, sticky=tk.E, padx=20, pady=5)

        tk.Button(bot_frame, text="Resume", width=10, command=self.passer_function())\
                .grid(row=0, column=2, sticky=tk.E, padx=20, pady=5)

        tk.Button(bot_frame, text="Add", width=10, command=my_controller.add_song_popup)\
                .grid(row=1, column=0, sticky=tk.E, padx=20, pady=5)

        tk.Button(bot_frame, text="Delete", width=10, command=self.passer_function())\
                .grid(row=1, column=1, sticky=tk.E, padx=20, pady=5)

        tk.Button(bot_frame, text="Queue", width=10, command=self.passer_function())\
                .grid(row=1, column=2, sticky=tk.E, padx=20, pady=5)

    def passer_function(self):
        pass

    # def display_song_name(self, name):
    #     """ Put the name in the name label """
    #     self._song_value['text'] = name

    def display_db_name(self, name):
        """ Put the db name in the top label """
        self._file_value['text'] = name



