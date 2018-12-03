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
#
# class MyHeap(object):
#     def __init__(self, initial=None, key=lambda x: x):
#         self.key = key
#         if initial:
#             self._data = [(key(item[0]), item) for item in initial]
#             heapq.heapify(self._data)
#         else:
#             self._data = []
#
#     def push(self, item):
#         heapq.heappush(self._data, (self.key(item[0]), item))
#
#     def pop(self):
#         return heapq.heappop(self._data)[1]
#
#     def peek(self, il):
#         if len(self._data) == 0:
#             return ""
#         else:
#             return self._data[il][1]
#
# l=MyHeap([["Abb",4],["ab",3]],str.lower)
# print(l.pop())
# print(l.push("f_*"))
# print(l._data[0][1])
#


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
    mod.start_index("D:\iretrival\corpus", "D:\iretrival\posting",False)
    # print(time.time() - starttime)



    # starttime = time.time()
    # merger=FileMerge.Merger("D:\iretrival\merge",1500)
    # merger.merge("posting")
    # print(time.time() - starttime)

    # with open("D:\iretrival\merge/dictionary.txt","r") as d:
    #     with open("D:\iretrival\merge/posing1.txt","r") as p:
    #         line=""
    #         for i in range(120000):
    #             line=d.readline()
    #         print(line)
    #         pointer=int(line.split(':')[1].split(',')[1].replace('\n',''))
    #
    #         p.seek(pointer)
    #         ans=p.readline()
    #         print(ans)




    # dict={}
    # with open("dictionary.txt", "r") as d:
    #     with open("posting.txt","r") as p:
    #
    #         d_lines = d.readlines()
    #         for line in d_lines:
    #             tmp = line.split(':')
    #             dict[tmp[0].lower()] = 0
    #         for i in range(150000):
    #             pic_line = p.readline()
    #             if pic_line.split(':')[0].lower() not in dict.keys():
    #                 print(str(i))
    #                 print("p----" + pic_line)
    #                 # print("p----"+post_line)
    #
    #                 break

