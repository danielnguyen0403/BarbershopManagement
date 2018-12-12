from tkinter import *
from tkinter import messagebox
from Backend import Database
from ServiceInterface import ServiceInterface

class customerInterface():
    """docstring for customerInterface."""
    def __init__(self):
        super(customerInterface, self).__init__()

        self.background = '#ECFBFB'

        self.window = Tk()
        self.window.title("Customer Interface")
        self.window.configure(background=self.background)
        self.database = Database()

        for x in range(60):
            Grid.columnconfigure(self.window, x+1, weight=2)

        for y in range(35):
            Grid.rowconfigure(self.window, y+1, weight=2)

        self.l1 = self.create_Label(0,0,"Phone")
        self.l2 = self.create_Label(1,0,"Name")
        self.l3 = self.create_Label(0,2,"Address")

        self.phone_text = StringVar()
        self.e1 = self.create_Entry(0,1,self.phone_text)

        self.name_text = StringVar()
        self.e2 = self.create_Entry(1,1,self.name_text)

        self.address_text = StringVar()
        self.e3 = self.create_Entry(0,3,self.address_text)

        self.lb = Listbox(self.window, height=10, width=35)
        self.lb.grid(row=2, column=0, rowspan=6, columnspan=2)

        self.sb = Scrollbar(self.window)
        self.sb.grid(row=2, column=2, rowspan=15)

        self.lb.configure(yscrollcommand=self.sb.set)
        self.sb.configure(command=self.lb.yview)

        self.lb.bind("<<ListboxSelect>>",self.select_item)

        select_image = PhotoImage(file="Select.png")
        self.b1 = self.create_Button(2,3,"Select",select_image,self.select_command)

        search_image = PhotoImage(file="Search.png")
        self.b2 = self.create_Button(3,3," Search Customer",search_image,self.search_command)

        add_image = PhotoImage(file="Add.png")
        self.b3 = self.create_Button(4,3," Add new Customer",add_image,self.add_command)

        viewAll_image = PhotoImage(file="ViewAll.png")
        self.b4 = self.create_Button(5,3," View All Customer",viewAll_image,self.view_command)

        close_image = PhotoImage(file="Back.png")
        self.b5 = self.create_Button(6,3," Close",close_image,quit)

        self.window.mainloop()

    def create_Button(self,row,column,text,image,command):
        font_text = ('Times New Roman','13','bold','italic')
        button = Button(self.window, text=text,image=image,compound="left", font=font_text, command=command)
        button.grid(row=row,column=column)
        return button

    def create_Label(self,row,col,text):
        font_text = ('Times New Roman','15','bold')
        label = Label(self.window,text=text,font=font_text,background=self.background)
        # self.l1.configure(background='#ECFBFB')
        label.grid(row=row,column=col)
        return label

    def create_Entry(self,row,col,text):
        entry = Entry(self.window, textvariable=text)
        entry.configure(background='#CEE7F1')
        entry.grid(row=row, column=col)
        return entry
    # def button_pressed(self,index):
    #     self.button[index].configure(bg='red')

    def select_item(self,event):
        if len(self.lb.curselection()) > 0:
            index = self.lb.curselection()[0]
            self.selected_tuple = self.lb.get(index)

    def select_command(self):
        try:
            messagebox.showinfo("Welcome","Hello "+(self.selected_tuple[1]))
            self.svInterface = ServiceInterface(self.selected_tuple[0])
        except NameError:
            messagebox.showinfo("Hint","You need to choose a name or phone")
        except AttributeError:
            messagebox.showinfo("Hint","You need to choose a name or phone")


    def view_command(self):
        self.lb.delete(0,END)
        self.e2.delete(0,END)
        self.e3.delete(0,END)
        self.e1.delete(0,END)
        for row in self.database.view_Customer():
            self.lb.insert(END,row)

    def add_command(self):
        self.lb.delete(0,END)
        temp = (self.name_text.get(),self.phone_text.get(),self.address_text.get())
        if (temp !=("","","")):
            self.database.insert_Customer(self.name_text.get(),self.phone_text.get(),self.address_text.get())
            self.e1.delete(0,END)
            self.e2.delete(0,END)
            self.e3.delete(0,END)
            messagebox.showinfo("Result","Customer is added!")
        else:
            messagebox.showinfo("Result","No data added. Put some information into the boxes")

    def search_command(self):
        self.lb.delete(0,END)
        for row in self.database.search_Customer(self.name_text.get(),self.phone_text.get(),self.address_text.get()):
            self.lb.insert(END,row)

# cust = customerInterface()
