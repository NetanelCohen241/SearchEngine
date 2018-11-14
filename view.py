from tkinter import *
from tkinter import filedialog

from model import model
import contoller



class view(object):

    def __init__(self, master, control):
        #view class members
        self.control = control
        self.master = master
        self.stemFlag = IntVar()
        #widdgets on the gui
        self.label = Label(self.master,text="path:")
        self.entry = Text(self.master,height=2, width=100)
        self.b_browse=Button(self.master, text="browse")
        self.b_reset=Button(self.master, text="Reset")
        self.b_dict=Button(self.master, text="Show Dicttionary")
        self.b_start=Button(self.master, text="Start")
        self.stemCheck=Checkbutton(self.master,text="Stemminig",variable=self.stemFlag)
        self.list=Listbox(self.master)
        self.list.insert(END,"a list")
        for item in ["one","two","three","four"]:
            self.list.insert(END,item)

        #grid layout
        self.label.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        self.b_browse.grid(row=0, column=2)
        self.b_reset.grid(row=2, column=0)
        self.b_dict.grid(row=2, column=1)
        self.b_start.grid(row=2, column=2)
        self.stemCheck.grid(row=1,column=0)
        self.list.grid(row=2)
        # bind widget to a function
        self.b_browse.bind("<1>", self.clik_on_browse)
        self.b_reset.bind("<1>", self.clik_on_reset)
        self.b_dict.bind("<1>", self.clik_on_dict)
        self.b_start.bind("<1>", self.clik_on_start)
        self.stemCheck.bind("<1>",self.checkbox_stemmer)
        self.list.bind("<Double-Button-1>",self.list_data)

        # self.entry.bind("<Button-3>", self.enter_handler)

    def clik_on_browse(self, event):
        path = filedialog.askopenfilename(filetypes=(("All Files", "*.*"), ("text files", "*.txt")))
        self.entry.delete('1.0', END)
        self.entry.insert(END, path)
        # self.entry.

    def clik_on_reset(self, event):
        print("Reset clicked")
        pass

    def checkbox_stemmer(self,event):
        if self.stemFlag.get() == 0:
            print("stemmer activated")
        else:
            print("stemmer deactivated")
        pass

    def clik_on_dict(self,event):
        pass

    def clik_on_start(self,event):
        pass

    def list_data(self,event):
        print(self.list.get(ACTIVE))
        pass


def main():
    root = Tk()
    root.title("my GUI")
    root.geometry("1000x400")
    Model = model()
    Control = contoller.controller( Model )
    View = view(root, Control)

    root.mainloop()


if __name__ == '__main__':
    main()