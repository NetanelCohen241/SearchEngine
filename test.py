import linecache
import multiprocessing
import threading
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
# print("Hello Sugar")
# from nltk.stem.snowball import EnglishStemmer
#
# e= EnglishStemmer()
# print("Stem" in "postingWithStemming")
#
# if __name__ == '__main__':
#     # num_of_None_capital=0
#     # total=0
#     # with open("D:\iretrival\posting\dictionary.txt","r") as f:
#     #     text = f.readlines()
#     #     for line in text:
#     #        if line.split()[3] == "0":
#     #            num_of_None_capital += 1
#     #        total += 1
#     # model.model
#     # print("number of None capital city: {0}\nTotal cities: {1}".format(num_of_None_capital,total))
#     # stop_words = {}
#     # with open("D:\iretrival\corpus" + "/stop_words.txt", "r") as sw:
#     #     lines = sw.readlines()
#     #     for line in lines:
#     #         stop_words[line[:len(line) - 1]] = ""
#     #     sw.close()
#     # p=Parse.Parser(stop_words)
#     # r=Reader.ReadFile("D:\iretrival\corpus")
#     # doc_list=r.startAction(0,1815)
#     # for doc in doc_list:
#     #     p.parse(doc.txt,False)
#     # print(p.count_numbers)
#
#     print(len(x))



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


def my_thread_job():
    # do any things here
    print ("thread start successfully and sleep for 5 seconds")
    time.sleep(5)
    print ("thread ended successfully!")


def cb(param1, param2):
    # this is run after your thread end
    print ("callback function called")
    print ("{} {}".format(param1, param2))


# example using BaseThread with callback
thread = BaseThread(
    name='test',
    target=my_thread_job,
    callback=cb,
    callback_args=("hello", "world")
)

thread.start()
print("hell00000000000000o")