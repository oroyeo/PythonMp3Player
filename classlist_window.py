import tkinter as tk


class ClasslistWindow(tk.Frame):

    def __init__(self, parent, close_callback, delete_callback, my_controller):
        """ Initialize the popup listbox window """
        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self._delete_cb = delete_callback

        parent.title('Class List')

        self.top_frame = tk.Frame(self.master)
        self.bot_frame = tk.Frame(self.master)
        self.top_frame.grid(row=0, padx=30, pady=10)
        self.bot_frame.grid(row=1, padx=30, pady=10)

        self.name_listbox = tk.Listbox(self.top_frame, width=20,
                                       selectmode=tk.BROWSE)
        self.name_scrollbar = tk.Scrollbar(self.top_frame, orient='vertical')
        self.name_scrollbar.config(command=self.name_listbox.yview)
        self.name_listbox.config(yscrollcommand=self.name_scrollbar.set)


        self.add_button = tk.Button(self.bot_frame, text="Add", width=10,
                                    command=my_controller.add_student_popup)
        self.close_button = tk.Button(self.bot_frame, text='Close', width=10,
                                   command=self._close_cb)

        self.delete_button = tk.Button(self.bot_frame, text='Delete', width=10,
                                   command=self._delete_cb)

        self.name_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.name_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


        self.add_button.pack()
        self.delete_button.pack()
        self.close_button.pack()


    def set_names(self, names):
        """ Update the listbox to display all names """
        self.name_listbox.delete(0, tk.END)
        for name in names:
            self.name_listbox.insert(tk.END, name)


