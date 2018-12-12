from tkinter import *
from Backend import Database

class ManagerInterface():
    """docstring for ManagerInterface."""
    def __init__(self):
        super(ManagerInterface, self).__init__()
        self.database = Database()
        self.window = Tk()
        # self.window.geometry("300x300")
        self.window.title("Manager Interface")

        self.l1 = Label(self.window,text="1. Service")
        self.l1.grid(row=0,column=0)
        self.l2 = Label(self.window,text="2. Barber")
        self.l2.grid(row=0,column=4)

        self.b1 = Button(self.window,text="AGREE",command=self.agree_command)
        self.b1.grid(row=7,column=1)
        self.b2 = Button(self.window,text="BACK",command=self.close)
        self.b2.grid(row=7,column=4)

        self.lb1 = Listbox(self.window, height=10, width=15)
        self.lb1.grid(row=1, column=0, rowspan=6, columnspan=2)

        self.sb1 = Scrollbar(self.window)
        self.sb1.grid(row=1, column=2, rowspan=15, columnspan=2)

        self.lb1.configure(yscrollcommand=self.sb1.set)
        self.sb1.configure(command=self.lb1.yview)

        self.lb1.bind("<<ListboxSelect>>",self.lb1_select_item)

        self.lb2 = Listbox(self.window, height=10, width=15)
        self.lb2.grid(row=1, column=4, rowspan=6, columnspan=2)

        self.sb2 = Scrollbar(self.window)
        self.sb2.grid(row=1, column=6, rowspan=15, columnspan=2)

        self.lb2.configure(yscrollcommand=self.sb2.set)
        self.sb2.configure(command=self.lb2.yview)

        self.lb2.bind("<<ListboxSelect>>",self.lb2_select_item)

        self.view_All_Services()
        self.window.mainloop()
