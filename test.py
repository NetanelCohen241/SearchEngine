import linecache
import multiprocessing
from multiprocessing import Pool


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
import model

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





# mod = model.model()
# # print ("hello")
# def index(pid):
#
#     idx = Indexer.Index("D:\iretrival\corpus", "D:\iretrival\posting",mod.cities_from_api)
#     idx.createIndex(False,pid)




# print("Number of cpu : ", multiprocessing.cpu_count())
#
# t=time.time()
# for i in range(0,100):
#     index(i)
# print(time.time()-t)


#
#
# for dirpath, dirnames, filenames in os.walk("."):
#     # print(dirnames)
#     # print(dirpath)
#     print(filenames)



# count=0
# dir=os.listdir("D:\iretrival\posting")
# for doc in dir:
#     with open("D:\iretrival\posting/"+doc,"r")as fin:
#         count+=len(fin.readlines())
#
# print(count)



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
    # starttime = time.time()
    # pool = Pool(processes=(multiprocessing.cpu_count())-1)
    # pool.map(index, numbers)
    # print(time.time()-starttime)

    # starttime = time.time()
    # for i in range(len(numbers)):
    #     index(numbers[i])
    # print(time.time() - starttime)

    #

    #
    #
    # starttime = time.time()
    # merger=FileMerge.Merger("D:\iretrival\merge",2000)
    # merger.merge()
    # print(time.time() - starttime)




    #
    # i=0
    # with open("pos.txt", "w+") as out:
    #     for i in range(168000):
    #         line = linecache.getline("postingTmp.txt",i)
    #         out.write(line)
    #         i += 1
    # out.close()

    # counter = 0
    # starttime = time.time()
    # with open("pos.txt", "w+") as out1:
    #     with open("postingTmp.txt", "r") as out2:
    #
    #         lines=out2.readlines()
    #         for i in range(168000):
    #             line = lines[i]
    #             out1.seek(counter)
    #             out1.write(line)
    #             counter += len(line)
    # # print(time.time() - starttime)
    # mod=model.model()
    # mod.start_index("D:\iretrival\corpus", "D:\iretrival\posting",False)
    starttime = time.time()
    merger=FileMerge.Merger("D:\iretrival\posting",1000)
    merger.merge("posting")
    print(time.time() - starttime)
    # with open("dictionary.txt","r") as d:
    #     with open("posting.txt","r") as p:
    #         line=""
    #         for i in range(148005):
    #             line=d.readline()
    #         print(line)
    #         pointer=int(line.split(':')[1].split(',')[1].replace('\n',''))
    #
    #         p.seek(pointer)
    #         ans=p.readline()
    #         print(ans)
    dict={}
    with open("dictionary.txt", "r") as d:
        with open("posting.txt","r") as p:

            d_lines = d.readlines()
            for line in d_lines:
                tmp = line.split(':')
                dict[tmp[0].lower()] = 0
            for i in range(150000):
                pic_line = p.readline()
                if pic_line.split(':')[0].lower() not in dict.keys():
                    print(str(i))
                    print("p----" + pic_line)
                    # print("p----"+post_line)

                    break




            p_lines=p.readlines()
            for line in p_lines:
                tmp=line.split(':')
                dict[tmp[0].lower()]=0
            for i in range(150000):
                dic_line = d.readline()
                if dic_line.split(':')[0].lower() not in dict.keys():
                    print(str(i))
                    print("d----"+dic_line)
                    # print("p----"+post_line)

                    break







