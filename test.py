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

import model
print("Hello Sugar")


if __name__ == '__main__':


    numbers=[]
    for i in range(0,45):
        numbers.append(i)
    # starttime = time.time()
    # pool = Pool(processes=(multiprocessing.cpu_count())-1)
    # pool.map(index, numbers)
    # print(time.time()-starttime)


    # starttime = time.time()
    mod=model.model()
    mod.start_index("D:\iretrival\corpus", "D:\iretrival\posting",True)
    # print(time.time() - starttime)
    #
    #
    # starttime = time.time()
    # merger=FileMerge.Merger("D:\iretrival\posting",2000)
    # merger.merge("posting")
    # # merger.upload_dictionary()
    # merger.city_index()
    # merger.language_index()
    # print(time.time() - starttime)



