from tkinter import *
from tkinter import messagebox
from Backend import Database
import datetime as dt

class ServiceInterface():
    """docstring for ServiceInterface."""
    def __init__(self,cid):
        super(ServiceInterface, self).__init__()

        self.background = '#ECFBFB'

        self.cid = cid
        self.database = Database()
        self.window = Tk()
        self.window.configure(background=self.background)
        self.window.geometry("400x500")
        self.window.title("Service Interface")

        self.l1 = self.create_Label(0,0,"1. Service")
        self.l2 = self.create_Label(3,0,"2. Barber")
        self.l3 = self.create_Label(1,2,"Cost:")
        self.l4 = self.create_Label(2,2,"Duration:")
        self.l5 = self.create_Label(1,3,"")
        self.l6 = self.create_Label(2,3,"")

        for x in range(60):
            Grid.columnconfigure(self.window, x+1, weight=2)

        for y in range(35):
            Grid.rowconfigure(self.window, y+1, weight=2)

        agree_image = PhotoImage(file="Agree.png")
        self.b1 = self.create_Button(4,2,"AGREE",agree_image,self.agree_command)

        back_image = PhotoImage(file="Back.png")
        self.b2 = self.create_Button(5,2,"BACK",back_image,self.close)

        self.lb1 = Listbox(self.window, height=10, width=25)
        self.lb1.grid(row=1, column=0, rowspan=2)
        self.lb2 = Listbox(self.window, height=10, width=25)
        self.lb2.grid(row=4, column=0,rowspan=2)

        self.sb1 = Scrollbar(self.window)
        self.sb1.grid(row=1, column=1, rowspan=2)
        self.sb2 = Scrollbar(self.window)
        self.sb2.grid(row=4, column=1, rowspan=2)

        self.lb1.configure(yscrollcommand=self.sb1.set)
        self.sb1.configure(command=self.lb1.yview)

        self.lb2.configure(yscrollcommand=self.sb2.set)
        self.sb2.configure(command=self.lb2.yview)

        self.lb1.bind("<<ListboxSelect>>",self.lb1_select_item)
        self.lb2.bind("<<ListboxSelect>>",self.lb2_select_item)

        self.view_All_Services()
        self.window.mainloop()

    def create_Button(self,row,column,text,image,command):
        font_text = ('Times New Roman','13','bold','italic')
        b = Button(self.window, text=text, compound="left", font=font_text, command=command)
        b.grid(row=row,column=column,sticky=N+S+E+W)
        return b

    def create_Label(self,row,col,text):
        font_text = ('Times New Roman','17','bold')
        label = Label(self.window,text=text,font=font_text,background=self.background)
        # self.l1.configure(background='#ECFBFB')
        label.grid(row=row,column=col)
        return label

    def lb1_select_item(self,event):
        if len(self.lb1.curselection()) > 0:
            self.lb2.delete(0,END)
            index = self.lb1.curselection()[0]
            self.selected_tuple_1 = self.lb1.get(index)
            service = self.database.search_Service(int(self.selected_tuple_1[0]),"","","")
            self.l5.configure(text="$"+str(service[0][2]))
            self.l6.configure(text=str(service[0][3])+" mins")
            list = self.database.employeesListForAService(self.selected_tuple_1[0])
            for row in list:
                self.lb2.insert(END,row[0])


    def lb2_select_item(self,event):
        if len(self.lb2.curselection()) > 0:
            index = self.lb2.curselection()
            self.selected_tuple_2 = self.lb2.get(index)

    def view_All_Services(self):
        self.lb1.delete(0,END)
        # for row in self.database.view_Service():
        #     self.lb1.insert(END,row)
        for row in self.database.view_Service():
            row = list(row)
            self.lb1.insert(END,str(row[0]) + ". " + row[1])


    def close(self):
        self.window.destroy()

    def agree_command(self):
        try:
            sid = self.selected_tuple_1[0]
            eid = list(self.database.search_Employee(self.selected_tuple_2,"","","")[0])
            eid = eid[0]
            date = dt.datetime.now().strftime("%x %H:%M")
            # insert into Choose table
            self.database.insert_Choose(self.cid,sid,eid,date)
            messagebox.showinfo("Result","You added to the service.")
            self.window.destroy()

        except AttributeError:
            return 0

# cus = ServiceInterface(3)
