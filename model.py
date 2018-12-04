import json
import requests

import multiprocessing
from multiprocessing import Pool

import os
import time

import FileMerge
from FileMerge import DictionaryElement
import Indexer

class IndexElement(object):

    def __init__(self, id, courpus_path, posting_path, stem, block_size, stop_words):
        self.id = id
        self.corpus_path = courpus_path
        self.posting_path = posting_path
        self.stem = stem
        self.block_size = block_size
        self.stop_words=stop_words


class model(object):

    def __init__(self):
        ##adding city file
        ##city dict{} from api
        self.term_dictionary = {}
        self.fake = ""
        self.cities_from_api = {}
        self.fill_cites()
        self.data = 5
        self.corpus_path=""
        self.posting_and_dictionary_path=""
        with open("language.txt", "w+") as fout:
            pass
        fout.close()

    def set_corpus_path(self, path):
        self.corpus_path = path

    def set_posting_and_dictionary_path(self, path):
        self.posting_and_dictionary_path = path
        with open(path+"/docs.txt", "w+") as out:
            out.write("Number            City            CityLocations             NumOfUniqeTerms    maxTf\n")
        out.close()

    def reset_memory(self, path):
        files_to_delete = os.listdir(path)
        for file in files_to_delete:
            os.remove(path + "/" + str(file))
        self.term_dictionary.clear()

    def read_dictionary_from_file(self,stem_flag):
        file_name= "/dictionary.txt" if not stem_flag else "/dictionaryWithStemming.txt"
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


    def fill_cites(self):
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
        idx = Indexer.Index(index_element.corpus_path, index_element.posting_path, self.cities_from_api, index_element.stop_words)
        idx.create_index(index_element.stem, index_element.id, index_element.block_size)

    def start_index(self, stem):
        stop_words = {}
        with open(self.corpus_path + "/stop_words.txt", "r") as sw:
            lines = sw.readlines()
            for line in lines:
                stop_words[line[:len(line) - 1]] = ""
            sw.close()
        files_number = len([word for word in os.listdir(self.corpus_path) if os.path.isdir(self.corpus_path + "/" + word)])
        s = files_number / 100
        tasks = []
        i = 0
        while i < int(s):
            index_element = IndexElement(i, self.corpus_path, self.posting_and_dictionary_path, stem, 100, stop_words)
            tasks.append(index_element)
            i += 1
        if files_number % 100 > 0:
            tasks.append(IndexElement(i, self.corpus_path, self.posting_and_dictionary_path, stem, files_number % 100, stop_words))
        starttime = time.time()
        pool = Pool(processes=(multiprocessing.cpu_count()))
        pool.map(self.index, tasks)
        print(time.time() - starttime)
        self.start_merge(stem)

    def start_merge(self, stem):

        starttime = time.time()
        merger = FileMerge.Merger(self.posting_and_dictionary_path, 2000)
        file_name="posting"
        if stem:
            file_name+="WithStemming"
        merger.merge(file_name)
        # merger.uploaddd_dictionary()
        merger.city_index()
        merger.language_index()
        print(time.time() - starttime)



