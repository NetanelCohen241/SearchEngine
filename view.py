import threading
from gc import callbacks
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import time

import Parse
from model import model
import contoller



class BaseThread(threading.Thread):
    def __init__(self, callback=None, callback_args=None, *args, **kwargs):
        target = kwargs.pop('target')
        super(BaseThread, self).__init__(target=self.target_with_callback, *args, **kwargs)
        self.callback = callback
        self.method = target
        self.callback_args = callback_args

    def target_with_callback(self):
        self.method()
        if self.callback is not None:
            self.callback(*self.callback_args)




class view(object):

    def __init__(self, master, control):
        #view classss members
        self.control = control
        self.master = master
        self.stemFlag = IntVar()
        self.corpus_path=""
        self.qry_path=""
        self.posting_path=""
        self.dic_in_RAM=False
        self.lang_chosse=StringVar(master)
        # choices = {'start indexing to see languages'}
        # self.popupMenu =  OptionMenu(self.master,choices,*choices)
        # Label(master, text="Choose a Language:").grid(row=2, column=0,sticky=E)

        # self.lang_chosse.set('English')  # set the default option
        #widdgets on the gui
        self.entry_corpus = Text(self.master, height=2, width=50)
        self.entry_posting_and_dict = Text(self.master, height=2, width=50)
        self.b_browse_corpus=Button(self.master,compound=LEFT, text="Browse corpus path",command=lambda : self.clik_on_browse_corpus() )
        self.b_browse_posting_and_dict=Button(self.master,compound=LEFT, text="Browse posting and dictionary path",command=lambda :  self.clik_on_browse_posting_and_dict())
        self.b_reset=Button(self.master, text="Reset",command=lambda : self.clik_on_reset())
        self.b_dict=Button(self.master,compound=LEFT, text="Show Dictionary",command=lambda :  self.display_dict())
        self.b_load_dictionary=Button(self.master,compound=LEFT, text="Load Dictionary",command=lambda : self.load_dictionary())
        self.b_start=Button(self.master, text="Start Indexing",command=lambda : self.clik_on_start())
        self.stemCheck=Checkbutton(self.master,text="Stemming?",variable=self.stemFlag)
        self.b_open_query = Button(self.master, compound=LEFT, text="Open query options", command=lambda: self.query_options())

        self.entry_corpus.grid(row=0, column=0)
        self.b_browse_corpus.grid(row=0, column=1,sticky=N+S+E+W)
        self.entry_posting_and_dict.grid(row=1, column=0)
        self.b_browse_posting_and_dict.grid(row=1, column=1,sticky=N+S+E+W)
        # self.popupMenu.grid(row=2, column=1,sticky=W)

        self.stemCheck.grid(row=2,column=0,sticky=W)
        self.b_dict.grid(row=5,column=0,columnspan =2,sticky=N+S+E+W)
        self.b_load_dictionary.grid(row=6, column=0,columnspan =2,sticky=N+S+E+W)
        self.b_reset.grid(row=7, column=0,columnspan =2,sticky=N+S+E+W)
        self.b_start.grid(row=8, column=0,columnspan =2,sticky=N+S+E+W)
        self.b_open_query.grid(row=9, column=0,columnspan =2,sticky=N+S+E+W)


    def query_options(self):

        if self.posting_path == "":
            messagebox.showerror("Error", "you must enter the posting and dictionary path before you can query")
            return
        self.load_dictionary()
        self.semanticFlag = IntVar()
        self.save_file_check = IntVar()
        self.detect_entities = IntVar()
        self.res_path=""
        self.qry_path=""
        self.qurey=""
        qurey_window = Toplevel(self.master)
        qurey_window.title("Query window")
        qurey_window.geometry("620x470")
        qurey_window.resizable(0, 0)
        self.semantic_check=Checkbutton(qurey_window,text="Semantic Treatment?",variable=self.semanticFlag)
        self.save_in_file_check=Checkbutton(qurey_window,text="save query results in a file?",variable=self.save_file_check,command=lambda: self.save_or_not())
        self.detect=Checkbutton(qurey_window,text="Detect Entities?",variable=self.detect_entities)
        self.q_box_manual=Text(qurey_window, height=2, width=30)
        self.q_box_from_path = Text(qurey_window, height=2, width=30)
        self.q_save_path = Text(qurey_window, height=2, width=30)
        self.b_run = Button(qurey_window, text="Run query", command=lambda: self.clik_on_run())
        self.b_browse_qurey = Button(qurey_window, compound=LEFT, text="Browse query path",command=lambda: self.clik_on_browse_query())
        self.b_save_to_file = Button(qurey_window,compound=LEFT, text="Browse", command=lambda: self.click_on_browse_resulat())
        self.b_run_from_file = Button(qurey_window,compound=LEFT, text="run qurey file", command=lambda: self.clik_on_run_from_file())
        Label(qurey_window,text="enter custom query: ").grid(row=0,column=0)
        Label(qurey_window,text="enter query from a file: ").grid(row=1,column=0)
        Label(qurey_window,text="enter result path: ",compound=LEFT).grid(row=2,column=0)
        self.q_box_manual.grid(row=0,column=1,sticky=N+S+E+W)
        self.b_run.grid(row=0,column=2,columnspan=2,sticky=N+S+E+W)
        self.q_box_from_path.grid(row=1,column=1,sticky=N+S+E+W,pady=30)
        self.b_browse_qurey.grid(row=1,column=2,sticky=N+S+E+W,pady=30)
        self.b_run_from_file.grid(row=1,column=3,sticky=N+S+E+W,pady=30)

        self.q_save_path.grid(row=2,column=1,sticky=S+W+E+W,pady=30)
        self.city_selector = Listbox(qurey_window, selectmode ="multiple")
        Label(qurey_window, text="Choose one or more cities: ",compound=CENTER).grid(row=5, column=1,columnspan=1,pady=15)
        self.b_save_to_file.grid(row=2,column=2,columnspan=2,sticky=N+S+E+W,pady=30)
        self.semantic_check.grid(row=4,column=0,stick='NSW',padx=20)
        self.save_in_file_check.grid(row=4,column=1,stick='NSW', padx=30)
        self.detect.grid(row=4,column=2,columnspan=2,stick='NSW', padx=20)
        self.b_save_to_file.config(state=DISABLED)
        vscroll = Scrollbar(qurey_window, orient=VERTICAL, command=self.city_selector.yview)
        vscroll.place(in_=self.city_selector, relx=1.0, relheight=1.0, bordermode="outside")
        self.city_selector['yscroll'] = vscroll.set
        self.city_selector.grid(row=6, column=1, columnspan=2, sticky=N + S + W, padx=60)

        self.fill_cities()

    def clik_on_browse_corpus(self):
        """
        אlistener for the browse corpus path button
        set the courpus path in the controller
        and show it to the user
        :param event:
        :return:
        """
        try:
            self.corpus_path = filedialog.askdirectory()
            self.control.set_corpus_path(self.corpus_path)
            self.entry_corpus.delete('1.0', END)
            self.entry_corpus.insert(END, self.corpus_path)
        except:
            pass


    def clik_on_browse_posting_and_dict(self):
        """
            אlistener for the browse post and dictionary path button
            set the posting path and dictionary path in the controller
            and show it to the user
            :param event:
            :return:
            """
        try:
            self.posting_path = filedialog.askdirectory()
            self.control.set_posting_path(self.posting_path)
            self.entry_posting_and_dict.delete('1.0', END)
            self.entry_posting_and_dict.insert(END, self.posting_path)
        except:
            pass


    def clik_on_reset(self):
        """
        listener for the reset button
        :param event:
        :return:
        """
        if self.posting_path == "":
            messagebox.showerror("Error","you must enter the posting and dictionary path before reset")
            return
        self.control.delete_files(self.posting_path)
        messagebox.showinfo("reset","All files from {0} were deleted".format(self.posting_path))

    def display_dict(self):
        """
        listener for the show dictionary path
        :param event:
        :return:
        """
        if not self.dic_in_RAM:
            messagebox.showerror("Error",
                                 "sorry, You must load the dictionary before you click 'show dictionary' button")
            return

        dict_window=Toplevel(self.master)
        dict_window.title("Dictionary information")
        dict_window.geometry("600x600")
        text=Text(dict_window, height=600, width=600)
        S = Scrollbar(dict_window)
        S.pack(side=RIGHT, fill=Y)
        S.config(command=text.yview)
        text.config(yscrollcommand=S.set)
        text.pack()
        to_display=self.control.get_dict_data()
        text.insert(END,to_display)

    def load_dictionary(self):
        """
        listener for the Load Dictionary button
        :return:
        """
        if self.posting_path == "":
            messagebox.showerror("Error", "you must enter the posting and dictionary path before Loadind dictionary")
            return
        try:
            self.control.load_dictionary(self.stemFlag.get()!=0)
            messagebox.showinfo("Load successful","Dictionary was loaded to the RAM")
            self.dic_in_RAM=True
        except:
            if self.stemFlag.get()==0:
                messagebox.showerror("Error",
                                     "there is no dictionary.txt file in the posting path")
            else:
                messagebox.showerror("Error",
                                     "there is no dictionaryWithStemming.txt file in the posting path")



    def clik_on_start(self):
        """
        listener for the start indexing button
        start the indexing process
        :return:
        """

        stemmer = self.stemFlag.get()!= 0
        if self.corpus_path=="" or self.posting_path=="":
            messagebox.showerror("input Error","sorry, You need to Select the following information:\ncourpus path, posting path")
            return
        messagebox.showinfo("Information","this action can take a while Please wait")
        self.start_time=time.time()
        try:
            self.control.set_stem(stemmer)
            thread = BaseThread(
                name='test',
                target=self.control.start_indexing,
                callback=self.cb,
                callback_args=(stemmer,"0")
            )
            thread.start()
            self.disabel_buttons()


            # self.control.start_indexing(stemmer)
        except Exception as e:
            messagebox.showerror("Error",repr(e))
            return

    def disabel_buttons(self):
        self.b_start.config(state=DISABLED)
        self.b_browse_corpus.config(state=DISABLED)
        self.b_browse_posting_and_dict.config(state=DISABLED)
        self.b_reset.config(state=DISABLED)
        self.b_dict.config(state=DISABLED)
        self.b_load_dictionary.config(state=DISABLED)
        self.stemCheck.config(state=DISABLED)


    def activate_buttons(self):
        self.b_start.config(state=ACTIVE)
        self.b_browse_corpus.config(state=ACTIVE)
        self.b_browse_posting_and_dict.config(state=ACTIVE)
        self.b_reset.config(state=ACTIVE)
        self.b_dict.config(state=ACTIVE)
        self.b_load_dictionary.config(state=ACTIVE)
        self.stemCheck.config(state=ACTIVE)

    def cb(self,stemmer,trash):
        index_time = time.time() - self.start_time
        num_of_docs = 0
        with open(self.posting_path + "/docs.txt" if not stemmer else self.posting_path + "/docsStem.txt") as f:
            num_of_docs = len(f.readlines())
        f.close()
        with open(
                self.posting_path + "/dictionary.txt" if not stemmer else self.posting_path + "/dictionaryWithStemming.txt") as f:
            num_of_terms = len(f.readlines())
        f.close()
        messagebox.showinfo("Indexing finished",
                            "{0} documents were indexed\n{1} uniqe term were created\nTotal time in sec: {2}"
                            .format(num_of_docs, num_of_terms, int(index_time)))
        self.activate_buttons()

    def clik_on_browse_query(self):
        try:
            self.qry_path = filedialog.askopenfilename()
            self.q_box_from_path.delete('1.0', END)
            self.q_box_from_path.insert(END, self.qry_path)
        except:
            pass

    def clik_on_run(self):
        city_choise=[]
        i= self.city_selector.curselection()
        idx=0
        for x in self.choices:
            if idx in i:
                city_choise.append(x)
            idx+=1
        qry = self.q_box_manual.get(1.0, END)
        self.control.rum_custom_query(qry, self.semanticFlag.get() == 0, city_choise)







    def fill_cities(self):
        self.choices = []
        with open(self.posting_path + "/cities.txt") as f:
            idx=0
            for i in f.readlines():
                city=i.split()[0].replace(":","")
                self.choices.append(city)
                self.city_selector.insert(idx, city)
                idx += 1
        f.close()

    def clik_on_run_from_file(self):
        if(self.b_browse_qurey == ""):
            messagebox.showerror("Path Error", " you need to provide qury file path")
            return;
        results = self.control.run_query_from_file(self.qry_path,self.semanticFlag.get() == 0)


    def click_on_browse_resulat(self):
        try:
            self.res_path = filedialog.askdirectory()
            self.control.set_posting_path(self.posting_path)
            self.entry_posting_and_dict.delete('1.0', END)
            self.entry_posting_and_dict.insert(END, self.posting_path)
        except:
            pass

    def save_or_not(self):
        flag= self.save_file_check.get()== 0
        if flag:
            self.b_save_to_file.config(state=DISABLED)
        else:
            self.b_save_to_file.config(state=ACTIVE)


def main():
    root = Tk()
    root.title("Search Engine")
    root.geometry("600x300")
    root.resizable(0,0)
    Model = model()
    Control = contoller.controller( Model )
    View = view(root, Control)

    root.mainloop()


if __name__ == '__main__':
    main()