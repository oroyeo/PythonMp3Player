import tkinter as tk


class QueueWindow(tk.Frame):

    def __init__(self, parent, close_callback, remove_callback, list):
        """ Initialize the popup listbox window """
        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self._remove_cb = remove_callback
        self._queue_list = list

        parent.title('Song Queue')

        self.top_frame = tk.Frame(self.master)
        self.bot_frame = tk.Frame(self.master)
        self.top_frame.grid(row=0, padx=30, pady=10)
        self.bot_frame.grid(row=1, padx=30, pady=10)

        self.queue_listbox = tk.Listbox(self.top_frame, width=20,
                                       selectmode=tk.BROWSE)
        self.queue_scrollbar = tk.Scrollbar(self.top_frame, orient='vertical')
        self.queue_scrollbar.config(command=self.queue_listbox.yview)
        self.queue_listbox.config(yscrollcommand=self.queue_scrollbar.set)


        self.remove_button = tk.Button(self.bot_frame, text="Remove", width=10,
                                    command=self._remove_cb)
        self.close_button = tk.Button(self.bot_frame, text='Close', width=10,
                                   command=self._close_cb)


        self.queue_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.queue_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)



        self.remove_button.pack()
        self.close_button.pack()


    def set_songs(self, names):
        """ Update the listbox to display all names """
        self.queue_listbox.delete(0, tk.END)
        for name in names:
            self.queue_listbox.insert(tk.END, name)


