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
        self.model.read_docs_details(stem)


    def load_dictionary_with_and_widtout(self):
        """
        this function load both dictionaries to the RAM
        :return:
        """
        self.model.read_dictionary_from_file(True)
        self.model.read_dictionary_from_file(False)
        self.model.read_docs_details(False)



    def run_query_from_file(self,path,semantic,city_choice,stem,resualt_path=""):
        """
        get given path of query file and run the quries onr bu one
        *****the qurey must be in a specific format****
        :param path: location of the quries file
        :param semantic: bool var that indicat to run the query with a semantic stetment or not
        :param city_choice: list of cities to filter by
        :param stem: bool var that indicate to run a stemming or not
        :param resualt_path: resualt path to save the data un trec eval format
        :return: dictionary with the nummber of the query as a key and list of relevant documents as the value
        """
        return self.model.run_queries_file(path,semantic,city_choice,stem,result_path=resualt_path)

    def rum_custom_query(self,qry, semantic_flag,city_choise,stem, result_path=""):
        """
        get a custome qry from the user and serch result
        :param qry: costume query as a string
        :param semantic_flag:  bool var that indicat to run the query with a semantic stetment or not
        :param city_choise: list of cities to filter by
        :param stem: bool var that indicate to run a stemming or not
        :param result_path: resualt path to save the data un trec eval format
        :return: dictionary with the nummber of the query as a key and list of relevant documents as the value
        """
        return self.model.rum_custom_query(qry,semantic_flag,city_choise,stem,result_path)
