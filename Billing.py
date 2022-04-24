from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tkn
import datetime
import os

import Backend
import EntryList
import Printing
import Json_data

# this get the date today
date_today = datetime.datetime.today()

# this is used  to assign the json default values
os.chdir(os.path.expanduser('~/Documents'))


class Bill_page:
    """When billing is called this class is assigned"""

    def __init__(self, master):
        super().__init__()
        # ________________
        self.master = master

        # initial assignments
        self.code_search = StringVar()
        self.main_type = StringVar()
        self.sub_type = StringVar()
        self.qty = StringVar()
        self.rate = StringVar()
        self.total_amount = StringVar()
        self.total_tables = IntVar()

        # Gets the no of tables to initial assign
        self.total_tables.set(Backend.General().getNoOfTables())

        # this is assigned to get the only integer values
        self.reg = self.master.register(callback)

        # ________________
        self.bill_tree = None
        self.table_places = None
        self.num = None
        self.amount = None
        self.win_ = None
        self.list_data = None

        # button for the in loop method
        self.button = []
        self.table_name = StringVar()
        self.table_num = IntVar()
        self.stock_object_id = StringVar()
        self.search_box_list = Backend.Billing().getItemsList()

        self.body_frame = Frame(self.master, height=690, width=1340)
        self.body_frame.place(x=0, y=0)

        # self.master.bind('<Control-Shift-Up>', lambda e: self.getTableData(1))

        self.details_frame = Frame(self.body_frame, width=400, height=550, bg="#C6C1B9")
        self.details_frame.place(x=10, y=120)

        self.bill_frame = Frame(self.body_frame, width=910, height=450, bg="#C6C1B9")
        self.bill_frame.place(x=420, y=120)

        edit_button = Button(self.body_frame, text='Edit', width=10, font="Helvetica 15 bold",
                             command=self.editFromBill)
        edit_button.place(x=450, y=600)

        delete_button = Button(self.body_frame, text='Delete', width=10, font="Helvetica 15 bold", fg="Red",
                               command=self.deleteFromBill)
        delete_button.place(x=680, y=600)

        submit_button = Button(self.body_frame, text='Submit', width=10, font="Helvetica 20 bold", fg="Blue",
                               command=self.submit_all)
        submit_button.place(x=900, y=600)

        Label(self.body_frame, text="Amount :", font="Helvetica 12 bold").place(x=1110, y=605)

        amount = Label(self.body_frame, textvariable=self.total_amount, font="Helvetica 20 bold ")
        amount.place(x=1200, y=600)

        # ___________Tables Fillings__________________________

        self.table_places = Frame(self.body_frame, width=1320, height=100, bg="#C6C1B9")
        self.table_places.place(x=10, y=10)

        x_position = 5
        y_position = 5
        for i in range(self.total_tables.get()):

            self.button.append(Button(self.table_places, text='Table ' + str(i + 1), font="Helvetica 10", width=12,
                                      command=lambda j=i: self.getTableData(j + 1)))
            self.button[i].place(x=x_position, y=y_position)
            x_position += 130
            if x_position > 1200:
                y_position += 32
                x_position = 5
        # check any tables are active are not
        self.checkStatus(0)

        # _______________________Details Fillings___________________________________________
        sel_table = Label(self.details_frame, textvariable=self.table_name, font="Helvetica 20 bold", bg="#C6C1B9")
        sel_table.place(x=140, y=70)

        # __________________________________________________________________________________________________________
        main_type = Label(self.details_frame, text="Main_Type :", font="Helvetica 10", bg="#C6C1B9")
        main_type.place(x=50, y=170)

        self.main_entry = Entry(self.details_frame, textvariable=self.main_type, font="Helvetica 10")
        self.main_entry.place(x=150, y=170)
        # suggested list box for values
        self.main_entry.bind("<KeyRelease>", self.searchIList)
        self.main_entry.bind("<Down>", lambda event: self.list_box.focus_set())

        # __________________________________________________________________________________________________________
        sub_type = Label(self.details_frame, text="Sub_type :", font="Helvetica 10", bg="#C6C1B9")
        sub_type.place(x=50, y=220)

        sub_entry = Entry(self.details_frame, textvariable=self.sub_type, font="Helvetica 10")
        sub_entry.place(x=150, y=220)

        # __________________________________________________________________________________________________________
        quantity = Label(self.details_frame, text="Qty :", font="Helvetica 10", bg="#C6C1B9")
        quantity.place(x=50, y=270)

        self.qty_entry = Entry(self.details_frame, textvariable=self.qty, font="Helvetica 10")
        self.qty_entry.place(x=150, y=270)
        self.qty_entry.config(validate="key", validatecommand=(self.reg, '%P'))

        # __________________________________________________________________________________________________________
        rate = Label(self.details_frame, text="Rate :", font="Helvetica 10", bg="#C6C1B9")
        rate.place(x=50, y=320)

        rate_entry = Entry(self.details_frame, textvariable=self.rate, font="Helvetica 10")
        rate_entry.place(x=150, y=320)
        rate_entry.config(validate="key", validatecommand=(self.reg, '%P'))

        add_to_tree = Button(self.details_frame, text='Add To Bill', font="Helvetica 10", width=12)
        add_to_tree.place(x=250, y=500)

        # ________________________Bill_Tree_____________________________________________
        bill_tree_fra = Frame(self.bill_frame, bg="gray")
        bill_tree_fra.place(x=0, y=0, width=910, height=450)

        self.bill_tree = ttk.Treeview(bill_tree_fra)
        self.bill_tree['show'] = 'headings'
        self.bill_tree['selectmode'] = "browse"

        scroll_y = Scrollbar(bill_tree_fra, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.bill_tree.yview)

        style = ttk.Style(self.bill_frame)
        style.theme_use("clam")
        style.map('Treeview',
                  background=[('selected', 'gray')])

        self.bill_tree['columns'] = ("ID", "Particulars", "Quantity", "Rate", "Amount")
        self.bill_tree["displaycolumns"] = ("Particulars", "Quantity", "Rate", "Amount")

        self.bill_tree.heading("ID", text="Stock_id", anchor=tkn.CENTER)
        self.bill_tree.heading("Particulars", text="Particulars", anchor=tkn.CENTER)
        self.bill_tree.heading("Quantity", text="Qty", anchor=tkn.CENTER)
        self.bill_tree.heading("Rate", text="Rate", anchor=tkn.CENTER)
        self.bill_tree.heading("Amount", text="Amount", anchor=tkn.CENTER)

        self.bill_tree.column("ID", width=80, minwidth=40, anchor=tkn.CENTER, stretch=NO)
        self.bill_tree.column("Particulars", width=300, minwidth=300, anchor=tkn.CENTER)
        self.bill_tree.column("Quantity", width=40, minwidth=40, anchor=tkn.CENTER)
        self.bill_tree.column("Rate", width=40, minwidth=40, anchor=tkn.CENTER)
        self.bill_tree.column("Amount", width=70, minwidth=70, anchor=tkn.CENTER, stretch=NO)

        self.bill_tree.pack(side='top', fill='both', expand=True)

        self.list_box = Listbox(self.details_frame, height=10, width=27)

        self.table_name.set('Select Table')
        self.qty_entry.bind('<Return>', self.addToBill)
        rate_entry.bind('<Return>', self.addToBill)
        add_to_tree.bind('<Button-1>', self.addToBill)
        rate_entry.bind('<Return>', self.addToBill)
        sub_entry.bind('<KeyRelease>', lambda event: self.list_box.place_forget())

    def getTableData(self, num):
        """there search for any active tables in existence and add data to those"""
        self.num = num
        self.table_name.set("Table :  " + str(self.num))
        self.table_num.set(self.num)
        self.main_entry.focus()

        self.bill_tree.delete(*self.bill_tree.get_children())
        data = Backend.Active().getTableData(self.table_num.get())
        if data:
            for j in data:
                for i in j['items']:
                    self.bill_tree.insert('', END, text="", values=(i[0], i[1], i[2], i[3], i[4]))

            self.total_amount.set(Backend.Billing().getTotalAmount(self.bill_tree))
        self.checkStatus(num)

    def checkStatus(self, num):
        """there get the status of active tables and selected tables"""
        active_tables = Backend.Billing().getActiveTables()
        for i in range(self.total_tables.get()):
            table_no = self.button[i].cget('text').split()
            if int(table_no[1]) in active_tables:
                self.button[i].config(bg="Green")
            else:
                self.button[i].config(bg="White")
        if num != 0:
            self.button[num - 1].config(bg="Gray")

    def addToBill(self, event):
        """there will add data to the bill tree """

        if self.table_num.get() != 0 and self.main_type.get() != '' and \
                self.sub_type.get() != '' and self.qty.get() != '' and self.rate.get() != '':
            exist_table = Backend.Active().checkTableExisted(self.table_num.get())

            if exist_table:
                tree_id = Backend.Billing().checkIfExisted(self.bill_tree, self.stock_object_id.get())
                if tree_id:
                    items = self.bill_tree.item(tree_id)['values']

                    new_qty = int(items[2]) + int(self.qty.get())
                    self.bill_tree.item(tree_id, text="", values=(items[0].strip(), items[1].strip(), new_qty,
                                                                  items[3], new_qty * items[3]))

                else:
                    combined = self.main_type.get().strip() + " - " + self.sub_type.get().strip()
                    self.bill_tree.insert('', END, text="",
                                          values=(self.stock_object_id.get(), combined,
                                                  int(self.qty.get()), self.rate.get(),
                                                  int(self.qty.get()) * int(self.rate.get())))
                    self.bill_tree.pack(side='top', fill='both', expand=True)

                list_data = Backend.Billing().convertTreeToList(self.bill_tree)
                self.total_amount.set(Backend.Billing().getTotalAmount(self.bill_tree))
                Backend.Active().updateTable(self.table_num.get(), list_data, self.total_amount.get())

            else:
                combined = self.main_type.get().strip() + " - " + self.sub_type.get().strip()
                self.bill_tree.insert('', END, text="",
                                      values=(self.stock_object_id.get(), combined,
                                              int(self.qty.get()), self.rate.get(),
                                              int(self.qty.get()) * int(self.rate.get())))
                self.bill_tree.pack(side='top', fill='both', expand=True)

                list_data = Backend.Billing().convertTreeToList(self.bill_tree)
                self.total_amount.set(Backend.Billing().getTotalAmount(self.bill_tree))
                Backend.Active().addTable(self.table_num.get(), list_data, self.total_amount.get())

            self.checkStatus(self.table_num.get())
            self.detailsClear()
            self.main_entry.focus()

        elif self.table_num.get() == 0:
            messagebox.showerror('Failed', 'No Table Selected')

        else:
            messagebox.showerror('Empty', 'Some fields are empty')

    def deleteFromBill(self):
        """these clear the data from the bill tree"""
        check = Backend.Billing().checkTreeSelected(self.bill_tree)

        if check:
            items = self.bill_tree.selection()
            for value in items:
                self.bill_tree.delete(value)
            self.total_amount.set(Backend.Billing().getTotalAmount(self.bill_tree))

        else:
            messagebox.showerror('No data', 'No data selected for deleting')

    def editFromBill(self):
        """this method edit data from the bill tree """
        check = Backend.Billing().checkTreeSelected(self.bill_tree)

        if check:
            items = self.bill_tree.selection()
            records = self.bill_tree.item(items, "values")

            # split the data by -
            type_of = records[1].split(" - ")

            # inserting the data to the field of main , sub, qty, rate
            self.stock_object_id.set(records[0])
            self.main_type.set(type_of[0])
            self.sub_type.set(type_of[1])
            self.qty.set(records[2])
            self.rate.set(records[3])

            # its delete the data from the bill tree
            self.deleteFromBill()

        else:
            messagebox.showerror('No data', 'No data selected for deleting')

    def submit_all(self):
        """this takes data from active table and send to submit bills"""
        existed = Backend.Billing().checkTreeExisted(self.bill_tree)

        if existed:
            try:
                Backend.Billing().submitData(self.table_num.get())
                data = Backend.Active().getTableData(self.table_num.get())
                for i in data:
                    self.print(i['amount'], i['items'])

                Backend.Active().delTable(self.table_num.get())
                self.detailsClear()

                for item in self.bill_tree.get_children():
                    self.bill_tree.delete(item)
                self.checkStatus(0)
                self.total_amount.set('')
                self.table_name.set('Select Table')
                self.table_num.set(0)
            except BaseException as msg:
                Backend.General.log_entry(307, 'Submit_all', msg)

        else:
            messagebox.showinfo('Error', 'No data in table')

    def print(self, amount, list_data):
        """this call the printing data"""
        self.amount = amount
        self.list_data = list_data
        try:
            Printing.Printing().print_data(self.amount, self.list_data)
        except BaseException as msg:
            Backend.General.log_entry(318, 'Print', msg)

        # this is top window for pinter pdf
        self.win_ = Toplevel()
        self.win_.geometry('170x500+400+160')
        self.win_.title('Pdf Reader')
        self.win_.configure(bg='white')

        Printing.Pdf_display().open_pdf_file(self.win_)

        print_but = Button(self.win_, text="Print", width=17, command=self.send_to_printer)
        print_but.place(x=15, y=420)
        cancel = Button(self.win_, text="Cancel", width=17)
        cancel.place(x=15, y=450)

        cancel.bind('<Button-1>', self.top_window_destroy)

        print_but.focus_set()

    def send_to_printer(self):
        """send pdf to printer"""
        success = Printing.Pdf_display().send_to_printer()
        if success:
            self.top_window_destroy(None)

    def top_window_destroy(self, event):
        """if initiated it will destroy all top layers"""

        try:
            self.win_.destroy()
        except BaseException as msg:
            pass

    # __________Search Data_______________________________________________

    def searchIList(self, event):
        """this gives the list box where the phone no are aligned"""

        # its align list box and bind some methods to it
        self.list_box.config(width=27)
        self.list_box.place(x=150, y=195)

        self.list_box.bind('<Leave>', self.destroyListBox)
        self.list_box.bind('<Double-1>', self.itemsSelected)
        self.list_box.bind('<Return>', self.itemsSelected)

        if self.search_box_list is not None:
            # this checks for the match in phone numbers list and assigned as matched list
            match = [i for i in self.search_box_list if self.main_type.get().lower() in i]

            # for inserting new data delete the old data
            self.list_box.delete(0, END)

            # this for add data to the listbox
            for c in match:
                self.list_box.insert(END, c)

            if not match:
                self.destroyListBox(None)

        if self.main_type.get() == "":
            self.destroyListBox(None)

    def itemsSelected(self, event):
        """when the no is selected from list box it aligned to
        the phone number and gives the data"""

        # this when selected the data to following happens
        for i in self.list_box.curselection():
            num = (self.list_box.get(i).split(" - "))
            # calls the data by main type and subtype as initial passing's
            data = Backend.Billing().getObjectId(num[0].title(), num[1].title())

            # by getting data back db and assigning those to the entries
            self.main_type.set(data['main'])
            self.stock_object_id.set(data['_id'])
            self.sub_type.set(data['sub'])
            self.qty.set(1)
            self.rate.set(data['rate'])
            self.qty_entry.focus()

            # after selecting the data and closing the list box
            self.destroyListBox(None)

    def destroyListBox(self, event):
        """this is the command when the list box to close"""
        try:
            self.list_box.place_forget()
        except BaseException:
            pass

    def detailsClear(self):
        """set the following values to null"""
        self.stock_object_id.set('')
        self.main_type.set('')
        self.sub_type.set('')
        self.qty.set('')
        self.rate.set('')

    def __del__(self):
        try:
            self.master.destroy()
        except BaseException as msg:
            print(msg)


class Stock:
    def __init__(self, master):
        """initial values assigning"""
        super().__init__()

        # initial assignments

        self.main_type = StringVar()
        self.sub_type = StringVar()
        self.rate = StringVar()
        self.master = master
        self.search = StringVar()
        self._id = StringVar()

        self.reg = self.master.register(callback)

        self.list_box1 = None
        self.selected = None
        self.add_button = None
        self.win_ = None
        self.searchMList = None
        self.searchSList = None

        # _____________________
        self.search_box_list = Backend.Stock().getTypesData('all')

        # ________________
        main_frame = Frame(self.master, height=690, width=1340)
        main_frame.place(x=0, y=0)

        top_frame = Frame(main_frame, width=1330, height=30)
        top_frame.place(x=5, y=5)

        body_frame = Frame(main_frame, width=1330, height=650)
        body_frame.place(x=5, y=45)

        search = Label(top_frame, text="Search :", width=12, font="Helvetica 10 bold")
        search.place(x=10, y=4)

        entry = Entry(top_frame, width=20, font="Helvetica 11 bold", textvariable=self.search)
        entry.place(x=120, y=4)
        entry.bind('<Return>', self.searchIt)

        ser_button = Button(top_frame, width=12, text="Search", font="Helvetica 8 bold")
        ser_button.place(x=300, y=4)
        ser_button.bind('<Button-1>', self.searchIt)
        ser_button.bind('<Return>', self.searchIt)

        add_new_item = Button(body_frame, width=12, font="Helvetica 10 bold", text="Add New Item",
                              command=self.addNewItem)
        add_new_item.place(x=25, y=600)

        modify_item = Button(body_frame, width=12, font="Helvetica 10 bold", text="Modify Item",
                             command=self.modifyItem)
        modify_item.place(x=170, y=600)

        delete_stock = Button(body_frame, width=12, font="Helvetica 10 bold", text="Delete Item",
                              command=self.deleteStock)
        delete_stock.place(x=315, y=600)

        self.tree_frame = Frame(body_frame)
        self.tree_frame.place(x=0, y=0, width=1330, height=550)

        scroll_y = Scrollbar(self.tree_frame, orient=VERTICAL)

        self.stock_tree = ttk.Treeview(self.tree_frame)
        self.stock_tree['show'] = 'headings'
        self.stock_tree['selectmode'] = "browse"

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.stock_tree.yview)

        style = ttk.Style(self.master)
        style.theme_use('clam')
        style.map('Treeview',
                  background=[('selected', 'gray')])

        self.stock_tree['columns'] = ("id", "Main_Type", "Sub_type", "rate", "Date")
        self.stock_tree["displaycolumns"] = ("Main_Type", "Sub_type", "rate", "Date")

        self.stock_tree.heading("id", text="id", anchor=tkn.CENTER)
        self.stock_tree.heading("Main_Type", text="Main_Type", anchor=tkn.CENTER)
        self.stock_tree.heading("Sub_type", text="Sub_type", anchor=tkn.CENTER)
        self.stock_tree.heading("rate", text="rate", anchor=tkn.CENTER)
        self.stock_tree.heading("Date", text="Date", anchor=tkn.CENTER)

        self.stock_tree.column("id", width=60, minwidth=60, anchor=tkn.CENTER)
        self.stock_tree.column("Main_Type", width=250, minwidth=250, anchor=tkn.CENTER)
        self.stock_tree.column("Sub_type", width=120, minwidth=120, anchor=tkn.CENTER)
        self.stock_tree.column("rate", width=200, minwidth=200, anchor=tkn.CENTER)
        self.stock_tree.column("Date", width=200, minwidth=200, anchor=tkn.CENTER)

        self.stock_tree.pack(side='top', fill='both', expand=True)
        self.treeData()

        self.list_box = Listbox(main_frame, height=10, width=27)

        # this is entry box assigned to search data
        EntryList.EntryBoxListLink(self.search_box_list, self.list_box, entry, self.search, 125, 33, 27, ser_button)

    def treeData(self):
        """this get values for the json files and fill the tree"""
        try:
            self.stock_tree.delete(*self.stock_tree.get_children())
        except BaseException as msg:
            print(msg)

        values = Backend.Stock().getAllStock()
        if values:
            i = 0
            for data in values:
                date = Backend.General().convertDateFormat(data['date'])
                self.stock_tree.insert('', i, text="", values=(data['_id'], data['main'],
                                                               data['sub'], data['rate'], date))
                i += 1
            self.stock_tree.pack(side='top', fill='both', expand=True)

    def searchIt(self, event):
        """search the value from the json data"""
        try:
            self.stock_tree.delete(*self.stock_tree.get_children())
        except BaseException:
            pass
        if self.search.get() == '':
            self.treeData()

        else:
            values = Backend.Stock().getSearchStock(self.search.get().title())
            if values:
                i = 0
                for data in values:
                    date = Backend.General().convertDateFormat(data['date'])
                    self.stock_tree.insert('', i, text="", values=(data['_id'], data['main'],
                                                                   data['sub'], data['rate'], date))
                    i += 1
                self.stock_tree.pack(side='top', fill='both', expand=True)

    def addNewItem(self):
        """this opens a top window to add new data as stock value"""
        self.destroyTopWindow()
        self.win_ = Toplevel()
        self.win_.geometry('400x250+400+300')
        self.win_.title("New Item")
        self.win_.grab_set()

        # main_type and sub_type list from the json data
        self.searchMList = Backend.Stock().getTypesData('main')
        self.searchSList = Backend.Stock().getTypesData('sub')

        self.main_type.set('')
        self.sub_type.set('')
        self.rate.set('')

        Label(self.win_, text='Main Type', width=12, font="Helvetica 15 bold").place(x=10, y=25)
        Label(self.win_, text='Sub Type', width=12, font="Helvetica 15 bold").place(x=10, y=70)
        Label(self.win_, text='Rate', width=12, font="Helvetica 15 bold").place(x=10, y=115)

        main_entry = Entry(self.win_, textvariable=self.main_type, width=12, font="Helvetica 15 bold")
        main_entry.place(x=180, y=25)

        sub_entry = Entry(self.win_, textvariable=self.sub_type, width=12, font="Helvetica 15 bold")
        sub_entry.place(x=180, y=70)

        rate_entry = Entry(self.win_, textvariable=self.rate, width=12, font="Helvetica 15 bold")
        rate_entry.place(x=180, y=115)
        rate_entry.config(validate="key", validatecommand=(self.reg, '%P'))

        self.add_button = Button(self.win_, text="Add Item", width=12, font="Helvetica 12 bold",
                                 command=self.confirmData)
        self.add_button.place(x=10, y=170)

        cancel_button = Button(self.win_, text="Cancel", width=12, font="Helvetica 12 bold",
                               command=self.cancelData)
        cancel_button.place(x=200, y=170)

        self.add_button.bind('<Return>', self.confirmData)
        self.add_button.bind('<Button-1>', self.confirmData)
        rate_entry.bind('<KeyRelease>', self.destroyListBox)

        self.list_box1 = Listbox(self.win_, height=10, width=27)

        EntryList.EntryBoxListLink(self.searchMList, self.list_box1, main_entry, self.main_type, 180, 57, 24,
                                   sub_entry)
        EntryList.EntryBoxListLink(self.searchSList, self.list_box1, sub_entry, self.sub_type, 180, 100, 24,
                                   rate_entry)
        main_entry.focus_set()

    def confirmData(self, event):
        """this conforms the data that add data to json data"""
        if self.main_type.get() != '' and self.sub_type.get() != '' and self.rate.get() != '':
            check_if = Backend.Stock().checkIfAlreadyExist(self.main_type.get().strip().title(),
                                                           self.sub_type.get().strip().title())
            if not check_if:
                confirm = Backend.Stock().addNew(self.main_type.get().strip().title(),
                                                 self.sub_type.get().strip().title(), self.rate.get())
                if confirm:
                    self.treeData()
                    self.main_type.set('')
                    self.sub_type.set('')
                    self.rate.set('')
                    self.destroyTopWindow()
                    messagebox.showinfo('Success', f'   {self.main_type.get().title()} \n added Successfully')
                    self.addNewItem()
                else:
                    messagebox.showerror('Failed', 'Failed In Stock Submitting')
            else:
                messagebox.showerror('Existed', 'Already same data existed')

    def cancelData(self):
        """cancel the top window of add new stock data"""
        try:
            self.win_.destroy()
        except BaseException:
            pass

    def modifyItem(self):
        """it opens data for modifying the data"""
        select = Backend.Billing().checkTreeSelected(self.stock_tree)
        if select:
            self.addNewItem()
            self.add_button["text"] = "Modify"

            self.selected = self.stock_tree.selection()
            values = self.stock_tree.item(self.selected, "values")

            self._id.set(values[0])
            self.main_type.set(values[1])
            self.sub_type.set(values[2])
            self.rate.set(values[3])

            self.add_button.bind('<Return>', self.confirmModify)
            self.add_button.bind('<Button-1>', self.confirmModify)
            self.add_button.bind('<Button-1>', self.confirmModify)
        else:
            messagebox.showerror('error', "No Data Selected")

    def confirmModify(self, event):
        """its conforms the modified data"""
        if self.main_type.get() != '' and self.sub_type.get() != '' and self.rate.get() != '':
            confirm = Backend.Stock().updateStock(self._id.get(), self.main_type.get().strip().title(),
                                                  self.sub_type.get().strip().title(), self.rate.get())
            if confirm:

                date = self.stock_tree.item(self.selected, "values")[4]
                self.stock_tree.item(self.selected, text="", values=(self._id.get(),
                                                                     self.main_type.get().strip().title(),
                                                                     self.sub_type.get().strip().title(),
                                                                     self.rate.get(), date))
                self.cancelData()
                messagebox.showinfo('Success', f'   {self.main_type.get()} \n successfully modified')

            else:
                messagebox.showerror('Failed', 'Failed In modifying data')

    def deleteStock(self):
        """its delete the stock from the json data"""
        select = Backend.Billing().checkTreeSelected(self.stock_tree)
        if select:
            items = self.stock_tree.selection()
            records = self.stock_tree.item(items, "values")
            ask = messagebox.askyesno('Delete Stock', "Do you want to delete this stock")
            if ask:
                Json_data.JsonFile().deleteJsonData("Stock", records[0])
                self.treeData()
                messagebox.showinfo("Sucessfully", "Sucessfully deleted stock")

        else:
            messagebox.showerror('No Data', 'No Data Selected for deleting')

    def destroyListBox(self, event):
        """this is the command when the list box to close"""
        try:
            self.list_box.place_forget()
        except BaseException:
            pass

        try:
            self.list_box1.place_forget()
        except BaseException:
            pass

    def destroyTopWindow(self):
        """It's for destroying the top window"""
        try:
            self.win_.destroy()
        except BaseException:
            pass


class Bills:
    """this is called for the bill details"""

    def __init__(self, master):
        super().__init__()

        self.win_ = None
        self.master = master
        self.search = StringVar()
        self.reg = self.master.register(callback)

        self.main_frame = Frame(self.master, height=690, width=1340)
        self.main_frame.place(x=0, y=0)

        top_frame = Frame(self.main_frame, width=1330, height=30)
        top_frame.place(x=5, y=5)

        body_frame = Frame(self.main_frame, width=1330, height=650)
        body_frame.place(x=5, y=45)

        search = Label(top_frame, text="Search :", width=12, font="Helvetica 10 bold")
        search.place(x=10, y=4)

        entry = Entry(top_frame, width=20, font="Helvetica 11 bold", textvariable=self.search)
        entry.bind('<Return>', self.searchIt)
        entry.place(x=120, y=4)
        entry.config(validate="key", validatecommand=(self.reg, '%P'))

        ser_button = Button(top_frame, width=12, text="Search", font="Helvetica 8 bold")
        ser_button.place(x=300, y=4)
        ser_button.bind('<Button-1>', self.searchIt)

        print_but = Button(body_frame, width=12, font="Helvetica 10 bold", text="Print Bill",
                           command=self.print)
        print_but.place(x=25, y=600)

        self.tree_frame = Frame(body_frame)
        self.tree_frame.place(x=0, y=0, width=1330, height=550)

        scroll_y = Scrollbar(self.tree_frame, orient=VERTICAL)

        self.bills_dt_tree = ttk.Treeview(self.tree_frame)
        self.bills_dt_tree['show'] = 'headings'
        self.bills_dt_tree['selectmode'] = "browse"

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.bills_dt_tree.yview)

        style = ttk.Style(self.master)
        style.theme_use('clam')
        style.map('Treeview',
                  background=[('selected', 'gray')])

        self.bills_dt_tree['columns'] = ("id", 'Sl No', "Table No", "Items", "Amount", "Initial Time", "Final Time")
        self.bills_dt_tree["displaycolumns"] = ('Sl No', "Table No", "Items", "Amount", "Initial Time", "Final Time")

        self.bills_dt_tree.heading("id", text="id", anchor=tkn.CENTER)
        self.bills_dt_tree.heading("Sl No", text="Sl No", anchor=tkn.CENTER)
        self.bills_dt_tree.heading("Table No", text="Table No", anchor=tkn.CENTER)
        self.bills_dt_tree.heading("Items", text="Items", anchor=tkn.CENTER)
        self.bills_dt_tree.heading("Amount", text="Amount", anchor=tkn.CENTER)
        self.bills_dt_tree.heading("Initial Time", text="Table Acquired", anchor=tkn.CENTER)
        self.bills_dt_tree.heading("Final Time", text="Table Closed", anchor=tkn.CENTER)

        self.bills_dt_tree.column("id", width=60, minwidth=60, anchor=tkn.CENTER)
        self.bills_dt_tree.column("Sl No", width=60, minwidth=60, anchor=tkn.CENTER)
        self.bills_dt_tree.column("Table No", width=250, minwidth=250, anchor=tkn.CENTER)
        self.bills_dt_tree.column("Items", width=200, minwidth=200, anchor=tkn.CENTER)
        self.bills_dt_tree.column("Amount", width=200, minwidth=200, anchor=tkn.CENTER)
        self.bills_dt_tree.column("Initial Time", width=200, minwidth=200, anchor=tkn.CENTER)
        self.bills_dt_tree.column("Final Time", width=200, minwidth=200, anchor=tkn.CENTER)

        self.bills_dt_tree.pack(side='top', fill='both', expand=True)
        self.bills_dt_tree.bind('<Double-1>', self.popWindow)
        self.getTreeDetails()

    def searchIt(self, event):
        """its search the data from the bills by table no"""
        try:
            self.bills_dt_tree.delete(*self.bills_dt_tree.get_children())
        except BaseException:
            pass
        if self.search.get() == "":
            self.getTreeDetails()
        else:
            values = Backend.Bills().getDataByTableNO(int(self.search.get()))
            if values:
                i = 0
                for data in values:
                    date1 = Backend.General().convertTimeFormat(data['initial time'])
                    date2 = Backend.General().convertTimeFormat(data['final_time'])
                    items_no = len(data['items'])

                    self.bills_dt_tree.insert('', i, text="", values=(data['_id'], data['sl_no'], data['table no'],
                                                                      str(items_no) + "  No of Items",
                                                                      data['amount'], date1, date2))
                    i += 1
                self.bills_dt_tree.pack(side='top', fill='both', expand=True)

    def getTreeDetails(self):
        """its gets the data from bills and assign"""
        try:
            self.bills_dt_tree.delete(*self.bills_dt_tree.get_children())
        except BaseException:
            pass

        values = Backend.Bills().getBillData()
        if values:
            i = 0
            for data in values:
                date1 = Backend.General().convertTimeFormat(data['initial time'])
                date2 = Backend.General().convertTimeFormat(data['final_time'])
                items_no = len(data['items'])

                self.bills_dt_tree.insert('', i, text="", values=(data['_id'], data['sl_no'], data['table no'],
                                                                  str(items_no) + "  No of Items",
                                                                  data['amount'], date1, date2))
                i += 1
            self.bills_dt_tree.pack(side='top', fill='both', expand=True)

    def popWindow(self, event):
        """its get the details by the table no and assigned in top window"""
        self.destroyTopWindow()

        data = Backend.Billing().checkTreeSelected(self.bills_dt_tree)

        # x, y = pyautogui.position()
        y = event.y
        if y > 300:
            y = 300
        if data:
            self.win_ = Toplevel()
            self.win_.title('Bill Details')
            self.win_.geometry("600x300+450+{}".format(y + 150))

            top_frame = Frame(self.win_, height=25, width=590, bg='white', relief="ridge")
            top_frame.place(x=5, y=5)

            # bill details
            details_frame = Frame(self.win_, bg='white', relief="ridge")
            details_frame.place(x=5, y=35, height=220, width=590)

            # cash are credit details
            bottom_frame = Frame(self.win_, height=25, width=590, bg='white', relief="ridge")
            bottom_frame.place(x=5, y=270)

            scroll_y = Scrollbar(details_frame, orient=VERTICAL)

            pop_tree = ttk.Treeview(details_frame)
            pop_tree['show'] = 'headings'
            pop_tree['selectmode'] = "browse"

            s = ttk.Style(details_frame)
            s.theme_use("clam")

            scroll_y.pack(side=RIGHT, fill=Y)
            scroll_y.config(command=pop_tree.yview)

            pop_tree['columns'] = ("Id", "Description", "Qty", "rate", "amount")
            pop_tree["displaycolumns"] = ("Description", "Qty", "rate", "amount")

            pop_tree.heading("Id", text="Id", anchor=tkn.CENTER)
            pop_tree.heading("Description", text="Description", anchor=tkn.CENTER)
            pop_tree.heading("Qty", text="Qty", anchor=tkn.CENTER)
            pop_tree.heading("rate", text="rate", anchor=tkn.CENTER)
            pop_tree.heading("amount", text="amount", anchor=tkn.CENTER)

            pop_tree.column("Id", width=110, minwidth=110, anchor=tkn.CENTER)
            pop_tree.column("Description", width=140, minwidth=140, anchor=tkn.CENTER)
            pop_tree.column("Qty", width=100, minwidth=100, anchor=tkn.CENTER)
            pop_tree.column("rate", width=110, minwidth=100, anchor=tkn.CENTER)
            pop_tree.column("amount", width=110, minwidth=100, anchor=tkn.CENTER)

            pop_tree.pack(side='top', fill='both', expand=True)

            items = self.bills_dt_tree.selection()
            records = self.bills_dt_tree.item(items, "values")

            data = Backend.Bills().getDataById(records[0])

            Label(top_frame, text=data['table no'], bg="white", font="Helvetica 12 bold").place(x=230, y=0)
            Label(bottom_frame, text=data['amount'], bg="white", font="Helvetica 12 bold").place(x=480, y=0)

            for j in data['items']:
                i = 0
                pop_tree.insert('', i, text="", values=(j[0], j[1], j[2], j[3], j[4]))
                i += 1
                pop_tree.pack(side='top', fill='both', expand=True)

    def destroyTopWindow(self):
        """its destroys the top window if any existed"""
        try:
            self.win_.destroy()
        except BaseException:
            pass

    def print(self):
        """open pdf and display data"""
        data = Backend.Billing().checkTreeSelected(self.bills_dt_tree)
        if data:
            items = self.bills_dt_tree.selection()
            records = self.bills_dt_tree.item(items, "values")

            values = Backend.Bills().getDataById(records[0])

            Printing.Printing().print_data(values['amount'], values['items'])
            self.win_ = Toplevel()
            self.win_.geometry('170x500+400+160')
            self.win_.title('Pdf Reader')
            self.win_.configure(bg='white')

            Printing.Pdf_display().open_pdf_file(self.win_)

            print_but = Button(self.win_, text="Print", width=17, command=self.send_to_printer)
            print_but.place(x=15, y=420)
            cancel = Button(self.win_, text="Cancel", width=17, command=self.destroyTopWindow)
            cancel.place(x=15, y=450)
            print_but.focus_set()
        else:
            messagebox.showerror("Not Selected", "Select a Bill To Print")

    def send_to_printer(self):
        """it send data to printer to print pdf"""
        success = Printing.Pdf_display().send_to_printer()
        if success:
            self.destroyTopWindow()


def callback(integer):
    """it returns only int values"""
    if integer.isdigit() or integer == "":
        return True
    else:
        return False
