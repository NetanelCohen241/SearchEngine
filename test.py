import linecache
import multiprocessing
from multiprocessing import Pool

import heapq

import os
import os.path

import Indexer
import time
import  Parse
import FileMerge

# mod = model.model()
# # print ("hello")
# def index(pid):
#
#     idx = Indexer.Index("D:\iretrival\corpus", "D:\iretrival\posting",mod.cities_from_api)
#     idx.createIndex(False,pid)
import Reader

import model
print("Hello Sugar")
from nltk.stem.snowball import EnglishStemmer

e= EnglishStemmer()
print("Stem" in "postingWithStemming")

if __name__ == '__main__':
    # num_of_None_capital=0
    # total=0
    # with open("D:\iretrival\posting\dictionary.txt","r") as f:
    #     text = f.readlines()
    #     for line in text:
    #        if line.split()[3] == "0":
    #            num_of_None_capital += 1
    #        total += 1
    # model.model
    # print("number of None capital city: {0}\nTotal cities: {1}".format(num_of_None_capital,total))
    # stop_words = {}
    # with open("D:\iretrival\corpus" + "/stop_words.txt", "r") as sw:
    #     lines = sw.readlines()
    #     for line in lines:
    #         stop_words[line[:len(line) - 1]] = ""
    #     sw.close()
    # p=Parse.Parser(stop_words)
    # r=Reader.ReadFile("D:\iretrival\corpus")
    # doc_list=r.startAction(0,1815)
    # for doc in doc_list:
    #     p.parse(doc.txt,False)
    # print(p.count_numbers)

    print(len(x))

