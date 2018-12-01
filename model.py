import json
import requests

import multiprocessing
from multiprocessing import Pool

import os
import time

import Indexer

class indexElement(object):

    def __init__(self,id,courpus_path,posting_path,stem):
        self.id=id
        self.courpus_path=courpus_path
        self.posting_path=posting_path
        self.stem=stem


class model(object):

    def __init__(self):
        ##adding city file
        ##city dict{} from api
        self.term_dictionary = {}
        self.fake=""
        self.cities_from_api={}
        self.fill_cites()
        self.data = 5
        with open("docs.txt", "w+") as out:
            out.write("Number            City            CityLocations             NumOfUniqeTerms    maxTf\n")
        out.close()
        with open("cites.txt", "w+") as fout:
            fout.write("City            stateName             currency          population          docId:locations\n")
        fout.close()

    def set_corpus_path(self,path):
        self.corpus_path=path

    def set_posting_and_dictionary_path(self,path):
        self.posting_and_dictionary_path=path


    def reset_memory(self,path):
        files_to_delete=os.listdir(path)
        for file in files_to_delete:
            os.remove(path+"/"+str(file))
        self.term_dictionary.clear()

    def dat(self):
        return self.data

    def add(self, value):
        print("old value:{0} ".format(self.data))
        self.data=int(value)
        print("new value:{0} ".format(self.data))

    def read_dictionary_from_file(self,path):
        with open(path+"/dictionary.txt","r") as f:
            txt=f.readlines()
            for line in txt:
                line=line.replace("\n","")
                tmp=line.split(":")
                data=tmp[1].split(",")
                self.term_dictionary[tmp[0]]=data

    def fill_cites(self):
        response = requests.get("https://restcountries.eu/rest/v2/all")
        json_content = json.loads(response.text)
        i = 0
        for t in json_content:
            currency=t["currencies"][0]["code"]
            pop=t["population"]
            state_name=t["name"]
            self.cities_from_api[t["capital"].lower()]=[str(state_name),str(currency),str(pop)]

    def get_dictionary(self):
        return self.term_dictionary

    def index(self, index_element):
        idx = Indexer.Index(index_element.courpus_path, index_element.posting_path, self.cities_from_api)
        idx.createIndex(index_element.stem, index_element.id)

    def start_index(self,corpus_path,posting_path,stem):
        processes = []
        tasks = []
        for i in range(0, 45):
            index_element=indexElement(i,corpus_path,posting_path,stem)
            tasks.append(index_element)
        starttime = time.time()
        pool = Pool(processes=(multiprocessing.cpu_count()) - 1)
        pool.map(self.index, tasks)
        print(time.time() - starttime)


