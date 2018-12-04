from tkinter import filedialog, END
from  model import model
import pandas as pd


class controller(object):
    def __init__(self, model=None):
        self.model=model

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
            key_value = key
            dic["term"].append(key)
            y = int(",".join(dictionary[key]).replace("\n", "").split(",")[-1])
            dic["term-freq"].append(y)
        index=["#"]*len(dic["term-freq"])
        data = {'         Term': list(dic["term"]), "         Term-frequency": list(dic["term-freq"])}
        df = pd.DataFrame(data=data,index=index)
        df = df.sort_values("         Term-frequency", 0, False)
        return df.to_string()

    def start_indexing(self,corpusPath,postingPath,stem_flag):
        """
        this function start the indexing
        :param corpusPath: location of the courpos
        :param postingPath: location of posting files
        :return:
        """
        print("start indexing...\nCourpus Path: {0}\nPosting Path: {1}\nStemmer: {2}".format(corpusPath,postingPath,stem_flag))
        self.model.start_index(corpusPath,postingPath,stem_flag)
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

    def load_dictionary(self,path):
        """
        reade dictionary to the RAM using the given path
        :param path: the path of the directory that contain dictionary.txt
        :return:
        """
        return self.model.read_dictionary_from_file(path)

