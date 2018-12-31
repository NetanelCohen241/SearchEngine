import json
import re

import requests

import multiprocessing
from multiprocessing import Pool

import os
import time

import FileMerge
import Parse
from FileMerge import DictionaryElement
import Indexer
from Search import Searcher


class IndexElement(object):

    def __init__(self, id, courpus_path, posting_path, stem, block_size, stop_words):
        self.id = id
        self.corpus_path = courpus_path
        self.posting_path = posting_path
        self.stem = stem
        self.block_size = block_size
        self.stop_words = stop_words


class model(object):

    def __init__(self):

        self.term_dictionary = {}
        self.fake = ""
        self.cities_from_api = {}
        self.documents = {}
        self.fill_cites()
        self.data = 5
        self.corpus_path = ""
        self.posting_and_dictionary_path = ""
        self.avgl=0
        self.stop_words = {}


    def set_corpus_path(self, path):
        """
        update the courpus path
        :param path: the updated path
        :return:
        """
        self.corpus_path = path
        with open(self.corpus_path + "/stop_words.txt", "r") as sw:
            lines = sw.readlines()
            for line in lines:
                self.stop_words[line[:len(line) - 1]] = ""
        sw.close()

    def set_posting_and_dictionary_path(self, path):
        """
        update the path of the posting and dictionary and open the docs.txt file
        :param path:
        :return:
        """
        self.posting_and_dictionary_path = path

    def reset_memory(self, path):
        """
        delete  al files in the given path
        :param path:
        :return:
        """
        files_to_delete = os.listdir(path)
        for file in files_to_delete:
            os.remove(path + "/" + str(file))
        self.term_dictionary.clear()

    def read_dictionary_from_file(self, stem_flag):
        """
        reade  from a txt  file nd bulding the term dictionary
        :param stem_flag: indicate if to reade stemmed dictionary or not
        :return:
        """
        file_name = "/dictionary.txt" if not stem_flag else "/dictionaryWithStemming.txt"
        with open(self.posting_and_dictionary_path + file_name, "r") as f:
            txt = f.readlines()
            for line in txt:
                l = line.split(":")
                pos = l[1].split(",")
                e = DictionaryElement(pos[0])
                e.pointer = int(pos[1])
                e.corpus_tf = int(pos[2])
                self.term_dictionary[l[0]] = e
        f.close()

    def read_docs_details(self, stem):

        with open(
                self.posting_and_dictionary_path + "/docsStem.txt" if stem else self.posting_and_dictionary_path + "/docs.txt",
                "r") as d:
            docs = d.readlines()
            del docs[0]
            for line in docs:
                tmp = line.split()
                self.documents[tmp[0]] = [tmp[1],tmp[2]]
                self.avgl+=int(tmp[1])
            self.avgl/=len(self.documents)


    def fill_cites(self):
        """
        do http request to API to get relevent information about capital cities
        """
        response = requests.get("https://restcountries.eu/rest/v2/all")
        json_content = json.loads(response.text)
        i = 0
        for t in json_content:
            currency = t["currencies"][0]["code"]
            pop = t["population"]
            state_name = t["name"]
            self.cities_from_api[t["capital"].lower()] = [str(state_name), str(currency), str(pop)]

    def get_dictionary(self):
        return self.term_dictionary

    def index(self, index_element):
        """
        this function start the indexing process
        :param index_element: all the parameter the function create_index need
        :return:
        """
        idx = Indexer.Index(index_element.corpus_path, index_element.posting_path, self.cities_from_api,
                            index_element.stop_words)
        idx.create_index(index_element.stem, index_element.id, index_element.block_size)

    def start_index(self, stem):
        """
        this function split the corpus to process
        :param stem:
        :return:
        """
        with open(
                self.posting_and_dictionary_path + "/docsStem" if stem else self.posting_and_dictionary_path + "/docs.txt",
                "w+") as out:
            out.write("Number            City           NumOfUniqeTerms    maxTf       Date\n")
        out.close()

        stop_words = {}
        try:
            with open(self.corpus_path + "/stop_words.txt", "r") as sw:
                lines = sw.readlines()
                for line in lines:
                    stop_words[line[:len(line) - 1]] = ""
            sw.close()

        except Exception:
            raise FileNotFoundError("the file stop_words.txt didn't found")

        files_number = len(
            [word for word in os.listdir(self.corpus_path) if os.path.isdir(self.corpus_path + "/" + word)])
        s = files_number / 46
        tasks = []
        i = 0
        while i < int(s):
            index_element = IndexElement(i, self.corpus_path, self.posting_and_dictionary_path, stem, 46, stop_words)
            tasks.append(index_element)
            i += 1
        if files_number % 46 > 0:
            tasks.append(IndexElement(i, self.corpus_path, self.posting_and_dictionary_path, stem, files_number % 46,
                                      stop_words))
        starttime = time.time()
        pool = Pool(processes=(multiprocessing.cpu_count()))
        pool.map(self.index, tasks)
        print(time.time() - starttime)
        self.start_merge(stem)

    def start_merge(self, stem):
        """
        merge the temporal posting files
        :param stem: if stemming exist in the files
        :return:
        """
        starttime = time.time()
        merger = FileMerge.Merger(self.posting_and_dictionary_path, 1000)
        file_name = "posting"
        if stem:
            file_name += "WithStemming"
        merger.merge(file_name)
        # merger.uploaddd_dictionary()
        merger.city_index()
        merger.language_index()
        print(time.time() - starttime)

    def run_queries_file(self, file_path, semantic, city_choice, result_path=""):

        with open(file_path , "r") as q:
            queries = dict()
            queries_list = q.read().split("</top>")
            for query in queries_list:
                if query == "":
                    continue
                tmp = query.split("<title>")
                query_number= tmp[0].split(':')[1].replace('\n','').replace(' ','')
                tmp= tmp[1].split("<desc>")
                query_content =tmp[0].replace('\n',' ')
                queries[query_number] = query_content+tmp[1].split("<narr>")[0][12:].replace('\n',' ')

            p = Parse.Parser(self.stop_words)
            searcher = Searcher(queries, self.term_dictionary, self.documents, self.avgl, self.posting_and_dictionary_path,p)

            results = searcher.run(city_choice)
            if result_path != "":
                self.write_results_to_disk(result_path,results)
            return results

    def rum_custom_query(self, query_content, semantic_flag, city_choice, result_path=""):

        p = Parse.Parser(self.stop_words)
        searcher = Searcher({}, self.term_dictionary, self.documents, self.avgl, self.posting_and_dictionary_path,p)
        results= searcher.run_query(query_content, city_choice)
        if result_path != "":
            self.write_results_to_disk(result_path, {"15":results})
        return results

    def write_results_to_disk(self, result_path,results):


        with open(result_path+"/results.txt","w+") as out:

            for query_num in results:
                for doc_num in results[query_num]:
                    out.write(str(query_num)+" 0 "+doc_num+" 1 42.38 mt\n")
            out.close()

