from tkinter import *


class EntryBoxListLink:
    def __init__(self, list_data='', list_box='', entry_box=None, set_variable='', x_axis=38, y_axis=52, width=20,
                 next_entry = None):
        self.list_data = list_data
        self.list_box = list_box
        self.entry_box = entry_box
        self.set_variable = set_variable
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.width = width

        def destroyListBox(event):
            """this is the command when the list box to close"""
            try:
                self.list_box.place_forget()
            except BaseException:
                pass

        def searchIList(event):
            """this gives the list box where the data no are aligned"""

            # its align list box and bind some methods to it
            self.list_box.config(width=self.width)
            self.list_box.place(x=self.x_axis, y=self.y_axis)

            self.list_box.bind('<Leave>', destroyListBox)
            self.list_box.bind('<Double-1>', itemsSelected)
            self.list_box.bind('<Return>', itemsSelected)

            if self.list_data is not None:
                # this checks for the match in phone numbers list and assigned as matched list
                match = [i for i in self.list_data if
                         (self.set_variable.get().lower() or self.set_variable.get().capitalize()) in i]

                # for inserting new data delete the old data
                self.list_box.delete(0, END)

                # this for add data to the listbox
                for c in match:
                    self.list_box.insert(END, c)

                if not match:
                    destroyListBox(None)

            if self.set_variable.get() == "":
                destroyListBox(None)

        def itemsSelected(event):
            """when the no is selected from list box it aligned to
            the phone number and gives the data"""

            # this when selected the data to following happens
            for i in self.list_box.curselection():
                self.set_variable.set(self.list_box.get(i))
                self.entry_box.focus_set()

                # after selecting the data and closing the list box
                destroyListBox(None)

            if next_entry is not None:
                next_entry.focus()

        def set_entry_focus(event):
            if list_box.curselection()[0] == 0:
                return self.entry_box.focus_set()

        self.entry_box.bind("<KeyRelease>", searchIList)
        self.entry_box.bind("<Down>", lambda event: self.list_box.focus_set())
