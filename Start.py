from tkinter import *
from ttkthemes import themed_tk as tk
import datetime
from tkinter import messagebox

import Backend
import Billing


class Start:
    """this comes the starting page of the application"""
    def __init__(self, master):
        self.master = master
        self.master.geometry("1366x768+0+0")
        self.master.title("Admin Page")
        self.master.config(bg="White")
        # this is assigned to the close button of the window
        self.master.protocol('WM_DELETE_WINDOW', self.Quit)

        # window assigning to full screen
        self.master.attributes("-fullscreen", True)
        self.master.bind('<Escape>', lambda event: self.master.attributes("-fullscreen", False))
        self.master.bind('<F11>', lambda event: self.master.attributes("-fullscreen", True))

        self.date_time = StringVar()
        self.bottom_frame = None

        # top frame to place some data
        top_frame = Frame(self.master, relief="sunken", height=40, width=1340)
        top_frame.place(x=10, y=5)

        self.bottom_frame = Frame(self.master, height=690, width=1340)
        self.bottom_frame.place(x=10, y=60)

        Label(self.bottom_frame, text="Welcome To \n Billing", font="Helvetica 40 bold").place(x=500, y=200)

        billing_button = Button(top_frame, width=20, height=1, text='Billing', command=self.billingPage)
        billing_button.place(x=5, y=5)

        stock_button = Button(top_frame, width=20, height=1, text='Stock', command=self.stockPage)
        stock_button.place(x=180, y=5)

        bills_button = Button(top_frame, width=20, height=1, text='Bills', command=self.bills)
        bills_button.place(x=355, y=5)

        Label(top_frame, textvariable=self.date_time, width=10, font="Helvetica 17 bold").place(x=1200, y=5)
        self.date_time.set(Backend.General().convertDateFormat(datetime.date.today().isoformat()))

    def billingPage(self):
        """this calls the billingPage"""
        self.frameDestroy()

        Billing.Bill_page(self.bottom_frame)

    def stockPage(self):
        """this calls the stock page"""
        self.frameDestroy()
        Billing.Stock(self.bottom_frame)

    def bills(self):
        """this calls the bills page"""
        self.frameDestroy()
        Billing.Bills(self.bottom_frame)

    def frameDestroy(self):
        """this is always called because it destroyed the intial frames so that n no of frames wont create
        to slow the api"""
        try:
            self.bottom_frame.destroy()
        except BaseException:
            pass
        self.bottom_frame = Frame(self.master, height=690, width=1340)
        self.bottom_frame.place(x=10, y=60)

    def Quit(self):
        """this is called when to close the application"""
        ask = messagebox.askokcancel('Quit', 'Do you Want To Exit')
        if ask:
            self.master.destroy()


def win():
    """initial initialization the page to view"""
    master = tk.ThemedTk()
    master.get_themes()
    master.set_theme("clam")
    Start(master)
    master.mainloop()


if __name__ == "__main__":
    win()
