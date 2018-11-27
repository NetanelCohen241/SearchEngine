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
        self.corpus_path=""
        self.posting_path=""
        #widdgets on the gui
        self.label = Label(self.master,text="corpus path:")
        self.labe2 = Label(self.master,text="posting and dictionary path:")
        # self.labe3 = Label(self.master,text="Dictionary:")
        self.entry_corpus = Text(self.master, height=2, width=100)
        self.entry_posting_and_dict = Text(self.master, height=2, width=100)
        self.b_browse_corpus=Button(self.master, text="browse")
        self.b_browse_posting_and_dict=Button(self.master, text="browse")
        self.b_reset=Button(self.master, text="Reset")
        self.b_dict=Button(self.master,compound=LEFT, text="Dictionary Show")
        self.b_load_dictionary=Button(self.master,compound=LEFT, text="Dictionary load")
        self.b_start=Button(self.master, text="Start")
        self.stemCheck=Checkbutton(self.master,text="Stemminig",variable=self.stemFlag)
        self.list=Listbox(self.master)
        self.list.insert(END,"a list")
        for item in ["one","two","three","four"]:
            self.list.insert(END,item)

        #grid layout
        self.label.grid(row=0, column=0)
        self.entry_corpus.grid(row=0, column=1)
        self.b_browse_corpus.grid(row=0, column=2)
        self.labe2.grid(row=1, column=0)
        self.entry_posting_and_dict.grid(row=1, column=1)
        self.b_browse_posting_and_dict.grid(row=1, column=2)
        self.stemCheck.grid(row=3,column=0)
        self.b_reset.grid(row=3, column=1)
        self.b_start.grid(row=4, column=1)
        self.list.grid(row=2,column=0)
        # self.labe3.grid(row=4, column=0)
        self.b_dict.grid(row=3,column=2)
        self.b_load_dictionary.grid(row=4, column=2)

        # bind widget to a function
        self.b_browse_corpus.bind("<1>", self.clik_on_browse_corpus)
        self.b_browse_posting_and_dict.bind("<1>", self.clik_on_browse_posting_and_dict)
        self.b_reset.bind("<1>", self.clik_on_reset)
        self.b_dict.bind("<1>", self.display_dict)
        self.b_start.bind("<1>", self.clik_on_start)
        self.stemCheck.bind("<1>",self.checkbox_stemmer)
        self.b_load_dictionary.bind("<1>",self.load_dictionary)
        self.list.bind("<Double-Button-1>",self.list_data)

        # self.entry.bind("<Button-3>", self.enter_handler)

    def clik_on_browse_corpus(self, event):
        self.corpus_path = filedialog.askdirectory()
        self.control.set_corpus_path(self.corpus_path)
        self.entry_corpus.delete('1.0', END)
        self.entry_corpus.insert(END, self.corpus_path)
        # self.entry.

    def clik_on_browse_posting_and_dict(self, event):
        self.posting_path = filedialog.askdirectory()
        self.control.set_posting_path(self.posting_path)
        self.entry_posting_and_dict.delete('1.0', END)
        self.entry_posting_and_dict.insert(END, self.posting_path)

    def clik_on_reset(self, event):
        self.control.delete_files(self.posting_path)
        pass

    def checkbox_stemmer(self,event):
        if self.stemFlag.get() == 0:
            print("stemmer activated")
        else:
            print("stemmer deactivated")
        pass

    def display_dict(self, event):
        to_display=self.control.get_dict_data(self.posting_path)
        pass
    def load_dictionary(self, event):
        self.control.load_dictionary(self.posting_path)
        pass

    def clik_on_start(self,event):
        stemmer = self.stemFlag.get()!=0
        self.control.start_indexing(self.corpus_path,self.posting_path,stemmer)
        pass

    def list_data(self,event):
        print(self.list.get(ACTIVE))
        pass


def main():
    root = Tk()
    root.title("my GUI")
    root.geometry("1100x400")
    Model = model()
    Control = contoller.controller( Model )
    View = view(root, Control)

    root.mainloop()


if __name__ == '__main__':
    main()