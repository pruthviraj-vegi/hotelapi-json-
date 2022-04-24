import os
import json
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from tkPDFViewer import tkPDFViewer as Pdf
from tkinter import filedialog
import win32api
import win32print

import Backend

os.chdir(os.path.expanduser('~/Documents'))


def coord(x, y, unit=1):
    x, y = x * unit, y * unit
    return x, y


class Printing:
    def __init__(self):
        self.amount = None
        self.bills = None

    @staticmethod
    def initialPath():

        try:
            with open("General.json", "r") as pf:
                list_data = json.load(pf)

            if os.path.isdir(list_data['Pdf path']):
                pass
            else:
                os.makedirs(list_data['Pdf path'])

            return list_data['Pdf path']

        except BaseException as msg:
            print(msg)
            data = {'No of Tables': 30, 'Pdf path': os.path.join(os.path.expanduser('~/Documents')),
                    'Printer': 'Default'}
            with open("General.json", "w") as pf:
                json.dump(data, pf)
            pf.close()
            return data['Pdf path']

    def print_data(self, amount, bills):
        self.amount = amount
        self.bills = bills
        file_path = os.path.join(Printing().initialPath(), 'bills.pdf')
        c = canvas.Canvas(file_path, pagesize=(1.85 * inch, 8.29 * inch), bottomup=0)
        c.setFont("Helvetica-Bold", 9)
        c_name = c.drawString(*coord(1, 5, mm), "Sri Renukamba Family Dhaba")

        c.setFont("Helvetica", 6)
        c.drawString(*coord(2, 10, mm), "Near Anil comforts wedding hall ")
        c.drawString(*coord(2, 14, mm), "Bangalore road")
        c.drawString(*coord(2, 18, mm), "Hiriyur")

        # lines for the billing data
        c.line(2, 70, 130, 70)  # 1st horizontal line

        y_axis = 28
        start_int = 1
        for i in self.bills:
            c.setFont("Helvetica", 8)
            # sl_no
            c.drawCentredString(*coord(3, y_axis, mm), "{}.".format(start_int))
            # dec
            c.drawString(*coord(7, y_axis, mm), "{}".format(i[1]))

            c.setFont("Helvetica-Bold", 8)
            # quantity
            c.drawCentredString(*coord(20, y_axis + 4, mm), "{}   X".format(i[2]))
            # rate
            c.drawCentredString(*coord(30, y_axis + 4, mm), "{}  =".format(i[3]))
            # final amount
            c.drawCentredString(*coord(40, y_axis + 4, mm), "{}".format(i[4]))

            y_axis += 8
            start_int += 1

            if y_axis > 200:
                c.line(2, 2, 130, 2)  # Bill Ending Line
                c.showPage()
                y_axis = 3

        c.line(*coord(1, y_axis, mm), *coord(44, y_axis, mm))  # Bill Ending Line

        # amount placement
        c.setFont("Helvetica", 10)
        c.drawRightString(*coord(32, y_axis + 4, mm), "Amount :")

        # Amount
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(*coord(40, y_axis + 4, mm),
                            "{}".format(Backend.General().convert_to_currency(self.amount)))

        c.showPage()
        c.save()


class Pdf_display:
    def __init__(self):
        self.master = None
        self._printer_name = None

    def open_pdf_file(self, window):
        self.master = window

        _path = Printing().initialPath()
        file_name = os.path.join(_path, 'bills.pdf')
        try:
            Pdf.ShowPdf.img_object_li.clear()
            if file_name != '':
                v1 = Pdf.ShowPdf()
                v2 = v1.pdf_view(self.master, pdf_location=open(file_name, 'r'), width=17, height=23)
                v2.place(x=10, y=10)
                self.master.grab_set()
        except BaseException as msg:

            file_name = filedialog.askopenfilename(initialdir=_path, title="Select Pdf File",
                                                   filetypes=(('PDF File', '.pdf'), ('PDF File', '.PDF')))

            if file_name != '':
                v1 = Pdf.ShowPdf()
                v2 = v1.pdf_view(self.master, pdf_location=open(file_name, 'r'), width=53, height=23)
                v2.place(x=10, y=10)
            else:
                pass

    def send_to_printer(self):
        file_name = os.path.join(Printing().initialPath(), 'bills.pdf')
        check_json = os.path.isfile('General.json')
        if check_json:
            with open("General.json", "r") as json_File:
                data = json.load(json_File)
                self._printer_name = data['Printer']

            try:
                win32print.SetDefaultPrinter(self._printer_name)
                win32api.ShellExecute(0, "print", file_name, '"%s"' % win32print.GetDefaultPrinter(), ".", 0)
                return True

            except BaseException as msg:
                Backend.General.log_entry(125, 'Pdf_display', msg)
