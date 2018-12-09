from tkinter import filedialog, END
from  model import model
import pandas as pd


class controller(object):
    def __init__(self, model=None):
        self.model=model
        self.stem=False

    def set_stem(self,stem):
        self.stem=stem

    def delete_files(self,path):
        """
        delete all posting file and dictinary from givem path
        :param: path - location of posting files and dictionary
        :return:
        """

        self.model.reset_memory(path)

    def get_dict_data(self):
        """
        :param path: path of the location of the ductionary.
        :return:
        """
        dictionary= self.model.get_dictionary()
        dic = {"term": [], "term-freq": []}
        for key in dictionary.keys():
            dic["term"].append(key)
            y = dictionary[key].corpus_tf
            dic["term-freq"].append(y)
        index=["#"]*len(dic["term-freq"])
        data = {'Term': list(dic["term"]), "Term-frequency": list(dic["term-freq"])}
        df = pd.DataFrame(data=data,index=index)
        # df = df.sort_values("Term-frequency", 0, False)
        return df.to_string()

    def start_indexing(self):
        """
        this function start the indexing
        :param corpusPath: location of the courpos
        :param postingPath: location of posting files
        :return:
        """
        print("start indexing...\nCourpus Path: {0}\nPosting Path: {1}\nStemmer: {2}".format(self.model.corpus_path, self.model.posting_and_dictionary_path,self.stem))
        self.model.start_index(self.stem)
        pass

    def set_corpus_path(self,path):
        """
        set the corpus path
        :param path:
        :return:
        """
        self.model.set_corpus_path(path)

    def set_posting_path(self,path):
        """
        set the corpus path
        :param path:
        :return:
        """
        self.model.set_posting_and_dictionary_path(path)

    def load_dictionary(self,stem):
        """
        reade dictionary to the RAM using the given path
        :param path: the path of the directory that contain dictionary.txt
        :return:
        """
        self.model.read_dictionary_from_file(stem)

