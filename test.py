import linecache
import multiprocessing
from multiprocessing import Pool
# import sys

import os
import os.path

import Indexer
import time
import  Parse
import FileMerge
# class Test():
#
#     def __init__(self,arg):
#         self.tmp=arg
#
#     def x(self):
#         p=[]
#         self.update(self,p)
#         p[4]=5
#         p[6]=7
#         print(p)
#
#
#     def update(self, self1, p):
#         p.extend([1, 2, 3, 4, 59, 6, 77, 8])
#
# t=Test(5)
# t.x()

x=Parse.Parser()
# print(x.parse("</F>",False))
# print(x.calcSize(["33/55"],0))

#
# r=Reader.ReadFile("D:\iretrival\corpus")
# t=time.time()
# list=r.startAction(100)
# ans=[]
# i=0
# for doc in list:
#     ans.extend(x.parse(doc.txt,False))
#     # print(i)
#     i+=1
#
# t=time.time()
# print(time.time()-t)

# print ("hello")
def index(pid):
    idx = Indexer.Index("D:\iretrival\corpus", "D:\iretrival\posting")
    idx.createIndex(False,pid)
# print("Number of cpu : ", multiprocessing.cpu_count())
#
# t=time.time()
# for i in range(0,100):
#     index(i)
# print(time.time()-t)
linecache.clearcache()
line = linecache.getline("testread.txt", 208)

#
#
# for dirpath, dirnames, filenames in os.walk("."):
#     # print(dirnames)
#     # print(dirpath)
#     print(filenames)

print("hello")

if __name__ == '__main__':

    xx=5
    processes = []
    # for pid in range(30,33):
    #     p = multiprocessing.Process(target=index, args=(pid,))
    #     processes.append(p)
    #     p.start()
    #
    # for process in processes:
    #     process.join()
    numbers=[]
    for i in range(0,45):
        numbers.append(i)
    starttime = time.time()
    pool = Pool(processes=(multiprocessing.cpu_count())-1)
    pool.map(index, numbers)
    print(time.time()-starttime)

    # starttime = time.time()
    # for i in range(len(numbers)):
    #     index(numbers[i])
    # print(time.time() - starttime)

    #
    starttime = time.time()
    merger=FileMerge.Merger("D:\iretrival\posting",2000)
    merger.merge()
    print(time.time() - starttime)








