from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


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
        self.lang_chosse=StringVar(master)
        choices = {'English', 'France', 'German', 'Italiano', 'Hebrew'}
        self.popupMenu = OptionMenu(master, self.lang_chosse, *choices)
        Label(master, text="Choose a Language:").grid(row=2, column=0,sticky=E)

        self.lang_chosse.set('English')  # set the default option
        #widdgets on the gui
        # self.label = Label(self.master,text="corpus path")
        # self.labe2 = Label(self.master,text="posting and dictionary path:")
        # self.labe3 = Label(self.master,text="Dictionary:")
        self.entry_corpus = Text(self.master, height=2, width=100)
        self.entry_posting_and_dict = Text(self.master, height=2, width=100)
        self.b_browse_corpus=Button(self.master,compound=LEFT, text="browse corpus path")
        self.b_browse_posting_and_dict=Button(self.master,compound=LEFT, text="Browse posting and dictionary path")
        self.b_reset=Button(self.master, text="Reset")
        self.b_dict=Button(self.master,compound=LEFT, text="Dictionary Show")
        self.b_load_dictionary=Button(self.master,compound=LEFT, text="Dictionary load")
        self.b_start=Button(self.master, text="Start Indexing")
        self.stemCheck=Checkbutton(self.master,text="Stemminig?",variable=self.stemFlag)
        # self.list=Listbox(self.master)
        # self.list.insert(END,"a list")
        # for item in ["one","two","three","four"]:
        #     self.list.insert(END,item)

        #grid layout
        # self.label.grid(row=0, column=0)
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
        self.corpus_path = filedialog.askdirectory()
        self.control.set_corpus_path(self.corpus_path)
        self.entry_corpus.delete('1.0', END)
        self.entry_corpus.insert(END, self.corpus_path)

    def clik_on_browse_posting_and_dict(self, event):
        self.posting_path = filedialog.askdirectory()
        self.control.set_posting_path(self.posting_path)
        self.entry_posting_and_dict.delete('1.0', END)
        self.entry_posting_and_dict.insert(END, self.posting_path)


    def clik_on_reset(self, event):
        self.control.delete_files(self.posting_path)


    def display_dict(self, event):
        dict_window=Toplevel(self.master)
        dict_window.title("dictionary information")
        dict_window.geometry("400x400")
        text=Text(dict_window, height=1000, width=400)
        S = Scrollbar(dict_window)
        S.pack(side=RIGHT, fill=Y)
        S.config(command=text.yview)
        text.config(yscrollcommand=S.set)
        text.pack()
        to_display=self.control.get_dict_data()
        data="Term          Frequency\n"
        for key in sorted(to_display.keys()):
            data += "{0}:           {1}\n".format(key,to_display[key][0])
        text.insert(END,data)

    def load_dictionary(self, event):
        self.control.load_dictionary(self.posting_path)
        pass

    def clik_on_start(self,event):
        stemmer = self.stemFlag.get()!=0
        if self.corpus_path=="" or self.posting_path=="":
            messagebox.showerror("input Error","sorry, You need to Select the following information:\ncourpus path, posting path")
            return
        self.control.start_indexing(self.corpus_path,self.posting_path,stemmer)


def main():
    root = Tk()
    root.title("Search Engine")
    root.geometry("1000x250")
    Model = model()
    Control = contoller.controller( Model )
    View = view(root, Control)

    root.mainloop()


if __name__ == '__main__':
    main()