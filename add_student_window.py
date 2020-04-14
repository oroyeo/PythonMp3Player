import tkinter as tk


class AddStudentWindow(tk.Frame):

    def __init__(self, parent, close_callback, add_callback):
        """ Initialize the popup add student window """
        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self._add_cb = add_callback

        parent.title('Add Student')

        self.top_frame = tk.Frame(master=parent)
        self.top_frame.grid(row=0, padx=30, pady=10)
        self.mid_frame = tk.Frame(master=parent)
        self.mid_frame.grid(row=1, column=0, padx=30, pady=10)
        self.entry_frame = tk.Frame(master=parent)
        self.entry_frame.grid(row=1, column=1, padx=30, pady=10)
        self.bot_frame = tk.Frame(master=parent)
        self.bot_frame.grid(row=2, padx=30, pady=10)

        tk.Label(self.mid_frame, text='Student ID:').grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Label(self.mid_frame, text='Student First Name:').grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Label(self.mid_frame, text='Student Last Name:').grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)

        self._new_id = tk.Entry(self.mid_frame, width=20)
        self._new_id.grid(row=0, column=1, sticky=tk.E)
        self._new_first_name = tk.Entry(self.mid_frame, width=20)
        self._new_first_name.grid(row=1, column=1, sticky=tk.E)
        self._new_last_name = tk.Entry(self.mid_frame, width=20)
        self._new_last_name.grid(row=2, column=1, sticky=tk.E)



        self.add_student_button = tk.Button(self.bot_frame, text="Save", width=10,
                                    command=self._add_cb)


        self.close_button = tk.Button(self.bot_frame, text='Cancel', width=10,
                                   command=self._close_cb)

        self.add_student_button.pack()
        self.close_button.pack()

    def get_form_data(self):
        """ Return a dictionary of form field values for this form """
        student_data = {"student_id": self._new_id.get(),
                "first_name": self._new_first_name.get(),
                "last_name": self._new_last_name.get()
                        }

        return student_data


