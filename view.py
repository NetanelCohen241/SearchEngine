from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import time

from model import model
import contoller



class view(object):

    def __init__(self, master, control):
        #view classss members
        self.control = control
        self.master = master
        self.stemFlag = IntVar()
        self.corpus_path=""
        self.posting_path=""
        self.dic_in_RAM=False
        self.lang_chosse=StringVar(master)
        choices = {'start indexing to see languades'}
        self.popupMenu =  OptionMenu(self.master,choices,*choices)
        Label(master, text="Choose a Language:").grid(row=2, column=0,sticky=E)

        # self.lang_chosse.set('English')  # set the default option
        #widdgets on the gui
        self.entry_corpus = Text(self.master, height=2, width=100)
        self.entry_posting_and_dict = Text(self.master, height=2, width=100)
        self.b_browse_corpus=Button(self.master,compound=LEFT, text="browse corpus path")
        self.b_browse_posting_and_dict=Button(self.master,compound=LEFT, text="Browse posting and dictionary path")
        self.b_reset=Button(self.master, text="Reset")
        self.b_dict=Button(self.master,compound=LEFT, text="Dictionary Show")
        self.b_load_dictionary=Button(self.master,compound=LEFT, text="Dictionary load")
        self.b_start=Button(self.master, text="Start Indexing")
        self.stemCheck=Checkbutton(self.master,text="Stemminig?",variable=self.stemFlag)

        self.entry_corpus.grid(row=0, column=0)
        self.b_browse_corpus.grid(row=0, column=1,sticky=N+S+E+W)
        # self.labe2.grid(row=1, column=0)
        self.entry_posting_and_dict.grid(row=1, column=0)
        self.b_browse_posting_and_dict.grid(row=1, column=1,sticky=N+S+E+W)
        self.popupMenu.grid(row=2, column=1,sticky=W)
        # self.list.grid(row=2,column=0,sticky=N+S+E+W)
        # self.labe3.grid(row=4, column=0)
        self.stemCheck.grid(row=2,column=0,sticky=W)
        self.b_dict.grid(row=5,column=0,columnspan =2,sticky=N+S+E+W)
        self.b_load_dictionary.grid(row=6, column=0,columnspan =2,sticky=N+S+E+W)
        self.b_reset.grid(row=7, column=0,columnspan =2,sticky=N+S+E+W)
        self.b_start.grid(row=8, column=0,columnspan =2,sticky=N+S+E+W)

        # bind widget to a function
        self.b_browse_corpus.bind("<1>", self.clik_on_browse_corpus)
        self.b_browse_posting_and_dict.bind("<1>", self.clik_on_browse_posting_and_dict)
        self.b_reset.bind("<1>", self.clik_on_reset)
        self.b_dict.bind("<1>", self.display_dict)
        self.b_start.bind("<1>", self.clik_on_start)
        self.b_load_dictionary.bind("<1>",self.load_dictionary)

        # self.entry.bind("<Button-3>", self.enter_handler)

    def clik_on_browse_corpus(self, event):
        try:
            self.corpus_path = filedialog.askdirectory()
            self.control.set_corpus_path(self.corpus_path)
            self.entry_corpus.delete('1.0', END)
            self.entry_corpus.insert(END, self.corpus_path)
        except:
            pass

    def clik_on_browse_posting_and_dict(self, event):
        try:
            self.posting_path = filedialog.askdirectory()
            self.control.set_posting_path(self.posting_path)
            self.entry_posting_and_dict.delete('1.0', END)
            self.entry_posting_and_dict.insert(END, self.posting_path)
        except:
            pass


    def clik_on_reset(self, event):
        self.control.delete_files(self.posting_path)


    def display_dict(self, event):
        if not self.dic_in_RAM:
            messagebox.showerror("Error",
                                 "sorry, You must load the dictionary before you click 'show dictionary' button")
            return

        dict_window=Toplevel(self.master)
        dict_window.title("dictionary information")
        dict_window.geometry("600x600")
        text=Text(dict_window, height=600, width=600)
        S = Scrollbar(dict_window)
        S.pack(side=RIGHT, fill=Y)
        S.config(command=text.yview)
        text.config(yscrollcommand=S.set)
        text.pack()
        to_display=self.control.get_dict_data()
        text.insert(END,to_display)

    def load_dictionary(self, event):
        try:
            self.control.load_dictionary(self.stemFlag.get()!=0)
            messagebox.showinfo("Load successful","Dictionary was loaded to the RAM")
            self.dic_in_RAM=True
        except:
            if self.stemFlag==0:
                messagebox.showerror("Error",
                                 "there is no dictionary.txt file in the posting path")
            else:
                messagebox.showerror("Error",
                                     "there is no dictionaryWithStemming.txt file in the posting path")

    def clik_on_start(self,event):
        stemmer = self.stemFlag.get()!=0
        if self.corpus_path=="" or self.posting_path=="":
            messagebox.showerror("input Error","sorry, You need to Select the following information:\ncourpus path, posting path")
            return
        messagebox.showinfo("Information","this action can take a while Please wait")
        start_time=time.time()
        self.control.start_indexing(stemmer)
        index_time=time.time()-start_time
        with open(self.posting_path + "/languages.txt") as f:
            choices = {'All'}
            for i in f.readlines():
                choices.add(i)
            choices=sorted(choices)
            self.popupMenu = OptionMenu(self.master, self.lang_chosse, *choices)
            self.popupMenu.grid(row=2, column=1, sticky=W)
        f.close()
        num_of_docs = 0
        with open(self.posting_path + "/docs.txt") as f:
            num_of_docs = len(f.readlines())
        f.close()
        with open(self.posting_path + "/dictionary.txt" if not stemmer else self.posting_path + "/dictionaryWithStemming.txt") as f:
            num_of_terms = len(f.readlines())
        f.close()
        messagebox.showinfo("Indexing finished", "{0} documents indexed\n{1} uniqe term were created\nTotal time in sec: {2}"
                             .format(num_of_docs, num_of_terms, int(index_time)))






def main():
    root = Tk()
    root.title("Search Engine")
    root.geometry("1000x450")
    root.resizable(0,0)
    Model = model()
    Control = contoller.controller( Model )
    View = view(root, Control)

    root.mainloop()


if __name__ == '__main__':
    main()