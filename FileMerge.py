import os
import linecache
import time
import heapq


class MyHeap(object):
    def __init__(self, initial=None, key=lambda x: x):
        self.key = key
        if initial:
            self._data = [(key(item[0]), item) for item in initial]
            heapq.heapify(self._data)
        else:
            self._data = []

    def push(self, item):
        heapq.heappush(self._data, (self.key(item[0]), item))

    def pop(self):
        return heapq.heappop(self._data)[1]

    def peek(self, i):
        if len(self._data) == 0:
            return ["",-1]
        else:
            return self._data[i][1]


class DictionaryElement(object):

    def __init__(self, posting_file):
        self.posting_file = posting_file
        self.corpus_tf = 0
        self.pointer = 0

    def to_string(self):
        return self.posting_file + "," + str(self.pointer) + "," + str(self.corpus_tf)


class Merger(object):

    def __init__(self, files_to_merge_path, chunk_size):

        self.files_to_merge_path = files_to_merge_path
        self.chunk_size = chunk_size
        self.dictionary = {}
        self.posting_block = {}
        self.chunks_list_to_merge = []
        self.pointers = []
        self.files_names = []
        open(self.files_to_merge_path + "/dictionary.txt", "w+")

    def merge(self, file_name):
        """
        This function merge the files into one sorted file - posting list
        :return:
        """
        self.files_names = [word for word in os.listdir(self.files_to_merge_path) if word.startswith(file_name)]
        terms = []
        self.upload_all_files_chunks()
        # insert into terms list the first term from each chunk
        for i in range(0, len(self.chunks_list_to_merge)):
            terms.append([self.chunks_list_to_merge[i][0][self.pointers[i]],i])

        self.start_merge(terms)
        self.write_dictionary_to_disk()
        self.__remove_tmp_files(file_name)

    def start_merge(self, terms):
        """
        This function implements the merge process.
        Upload the all files in chunks.
        Iterate over the all chunks.( Each chunk is sorted)
        The merge: find the minimum value among the all chunks, merge the minimum value content for each file that the minimum is in it.
        Save the merged data into class member postingBlock(dictionary)
        And so on ,until we upload the all chunks.
        :param terms:
        :return:
        """
        terms = MyHeap(terms, str.lower)
        posting_list_pointer = 0
        posting_id = 1
        while not self.has_finished():

            term, merge_content = self.next_term(terms)

            self.posting_block[term] = merge_content
            total_freq=self.__calculate_total_tf(merge_content)
            self.__add_to_dictionary(term, "posing" + str(posting_id) + ".txt", posting_list_pointer, total_freq)
            posting_list_pointer += len(term) + len(merge_content) + 3

            if posting_list_pointer > 15500000:
                self.__write_merge_content_to_disk("posing" + str(posting_id) + ".txt")
                posting_id += 1
                posting_list_pointer=0
        self.__write_merge_content_to_disk("posing" + str(posting_id) + ".txt")

    def next_term(self, terms):

        next = ""
        merge = ""
        term = ""
        is_lower = False

        while not self.has_finished() and term.lower() == next.lower():
            min_term = terms.pop()
            t = min_term[0]
            if self.dictionary.__contains__(t):
                print("5")
            min_idx = min_term[1]
            pos = self.pointers[min_idx] % self.chunk_size
            merge += " " + self.chunks_list_to_merge[min_idx][1][pos].replace('\n', "")

            if not is_lower:
                if t.islower() or t[0].islower():
                    term = t
                    is_lower = True
                elif t[0].isupper():
                    term = t.upper()
                else:
                    term = t

            self.pointers[min_idx] += 1
            if self.pointers[min_idx] % self.chunk_size == 0:
                self.upload_file_chunk(min_idx)
            if self.pointers[min_idx] != -1:
                terms.push([self.chunks_list_to_merge[min_idx][0][self.pointers[min_idx] % self.chunk_size],min_idx])
            next = terms.peek(0)[0]

        return term, merge

    def upload_all_files_chunks(self):
        """
        This function upload chunk(of lines) from each file(postinglist
        :return:
        """
        for i in range(len(self.files_names)):
            self.chunks_list_to_merge.append(0)
            self.pointers.append(0)
            self.upload_file_chunk(i)

    def upload_file_chunk(self, file_number):

        term_dict = self.read_lines(file_number, self.pointers[file_number], self.chunk_size)
        self.chunks_list_to_merge[file_number] = term_dict

    def read_lines(self, file_number, start, how_many_to_read):
        """
        This function read specific lines from a file.
        :param file_number:
        :param start: from which line start to read
        :param how_many_to_read:
        :return: dictionary
        """
        file_name = self.files_names[file_number]
        keys = []
        values = []
        if start < 0: return ''
        current_line_number = 0
        eof = True
        for line in open(file_name, "r", -1, "utf-8"):
            if start <= current_line_number < start + how_many_to_read:
                tmp = line.split(':')
                keys.append(tmp[0])
                values.append(tmp[1].replace('\n', ''))
                eof = False
            current_line_number += 1
            if current_line_number == start + how_many_to_read:
                break
        if eof:
            self.pointers[file_number] = -1
            return [[""], [""]]
        if current_line_number != start + how_many_to_read:
            for i in range(0, how_many_to_read + start - current_line_number):
                keys.insert(0, "")
                values.insert(0, "")
            self.pointers[file_number] = how_many_to_read + start - (current_line_number % how_many_to_read)

        return [keys, values]


    def read_lines2(self, file_number, start, how_many_to_read):
        """
        This function read specific lines from a file.
        :param file_number:
        :param start: from which line start to read
        :param how_many_to_read:
        :return: dictionary
        """
        file_name = self.files_names[file_number]
        keys = []
        values = []
        if start < 0: return ''
        current_line_number = start
        eof = True
        for i in range(start,how_many_to_read):
            line=linecache.getline(file_name,i)
            if line== "":
                break
            tmp = line.split(':')
            keys.append(tmp[0])
            values.append(tmp[1].replace('\n', ''))
            eof = False
            current_line_number += 1

        if eof:
            self.pointers[file_number] = -1
            return [[""], [""]]
        if current_line_number != start + how_many_to_read:
            for i in range(0, how_many_to_read + start - current_line_number):
                keys.insert(0, "")
                values.insert(0, "")
            self.pointers[file_number] = how_many_to_read + start - (current_line_number % how_many_to_read)

        return [keys, values]


    def has_finished(self):

        ans = True
        for i in range(len(self.pointers)):
            if self.pointers[i] != -1:
                ans = False
                break
        return ans

    def __write_merge_content_to_disk(self, file_name):
        """
        This function writes the posting list into the disc
        :return:
        """
        with open(self.files_to_merge_path + "/" + file_name, "w+") as out:
            for key in self.posting_block.keys():
                out.write(key + ":")
                out.write(self.posting_block[key] + '\n')
        out.close()
        self.posting_block = {}

    def write_dictionary_to_disk(self):
        """
        This function writes the dictionary into the disc
        :return:
        """
        with open(self.files_to_merge_path + "/dictionary.txt", "w+") as out:
            for key in self.dictionary.keys():
                out.write(key + ":")
                out.write(self.dictionary[key].to_string() + '\n')
        out.close()

    def __add_to_dictionary(self, term, posting_file, posting_list_pointer, tf):

        e = DictionaryElement(posting_file)
        e.pointer = posting_list_pointer
        e.corpus_tf=tf
        self.dictionary[term] = e


    def __calculate_total_tf(self, line):

        term_corpus_frequency = 0
        try:
            elements = line.split()
            for i in range(len(elements)):
                term_corpus_frequency += int(str(elements[i].split(',')[1]))
        except:
            return 0
        return term_corpus_frequency

    def city_index(self):

        city_files = [word for word in os.listdir(os.getcwd()) if word.startswith("city")]
        cities = {}
        # build cities dictionary
        for i in range(len(city_files)):
            with open(city_files[i], "r") as c:
                lines = c.readlines()
                for line in lines:
                    city = line.split(":")
                    if not cities.__contains__(city[0]):
                        cities[city[0]] = city[1] + " " + str(self.dictionary[city[0].upper()].pointer)

        # write cities to disk
        with open(self.files_to_merge_path + "/cities.txt", "w+") as c:
            for city in cities:
                c.write(city + ": " + cities[city])
            c.close()
        self.__remove_tmp_files("city")

    def __remove_tmp_files(self, file_name):

        files = [word for word in os.listdir(os.getcwd()) if word.startswith(file_name)]
        for file in files:
            os.remove(file)

#
# import os
# import linecache
# import heapq
#
# class DictionaryElement(object):
#
#     def __init__(self,postingFile):
#         self.postingFile=postingFile
#         self.corpus_tf=0
#         self.pointer=0
#
#     def toString(self):
#         return self.postingFile+","+str(self.pointer)+","+str(self.corpus_tf)
#
#
# class Merger(object):
#
#     def __init__(self, filesToMergePath, chunkSize):
#
#         self.filesToMergePath = filesToMergePath
#         self.chunkSize = chunkSize
#         self.dictionary = {}
#         self.postingBlock = {}
#         self.chunksListToMerge = []
#         self.pointers = []
#         self.filesNames=[]
#         open("postingTmp.txt", "w+")
#         open("dictionary.txt", "w+")
#
#     def merge(self, file_name):
#         """
#         This function merge the files into one sorted file - posting list
#         :return:
#         """
#         self.filesNames = [word for word in os.listdir(self.filesToMergePath) if word.startswith(file_name)]
#         terms = []
#         self.uploadAllFilesChunks()
#         # insert into terms list the first term from each chunk
#         for i in range(0, len(self.chunksListToMerge)):
#             terms.append(self.chunksListToMerge[i][0][self.pointers[i]])
#
#         self.startMerge(terms)
#         self.writeMergeContentToDisk("postingTmp.txt")
#         # self.writeDictionaryToDisk()
#         print("merge is done")
#         # self.updatePointers()
#         self.clearUpperCase()
#         self.writeDictionaryToDisk()
#
#     def startMerge(self, terms):
#         """
#         This function implements the merge process.
#         Upload the all files in chunks.
#         Iterate over the all chunks.( Each chunk is sorted)
#         The merge: find the minimum value among the all chunks, merge the minimum value content for each file that the minimum is in it.
#         Save the merged data into class member postingBlock(dictionary)
#         And so on ,until we upload the all chunks.
#         :param terms:
#         :return:
#         """
#         postingListPointer = 1
#         while not self.hasFinished():
#
#             minTermIdx = self.findMin(terms)
#             term = self.chunksListToMerge[minTermIdx][0][self.pointers[minTermIdx] % self.chunkSize]
#
#             self.postingBlock[term] = ""
#             # iterate over each chunk, in every chunk that the term exists, append its content to postingBlock
#             for i in range(0, len(self.chunksListToMerge)):
#                 # check if we already uploaded the all file
#                 if self.pointers[i] == -1:
#                     continue
#                 pos = self.pointers[i] % self.chunkSize
#                 if self.chunksListToMerge[i][0][pos] == term:
#                     #append term content to posting list
#                     self.postingBlock[term] += self.chunksListToMerge[i][1][pos]
#                     self.pointers[i] += 1
#                     if self.pointers[i] % self.chunkSize == 0:
#                         self.uploadFileChunk(i)
#                     if self.pointers[i] != -1:
#                         terms[i] = self.chunksListToMerge[i][0][self.pointers[i] % self.chunkSize]
#
#
#             self.AddToDictionary(term, postingListPointer)
#
#             postingListPointer += 1
#             # if postingListPointer % 500000 == 0:
#             #     self.writeMergeContentToDisk("postingTmp.txt")
#
#     def uploadAllFilesChunks(self):
#         """
#         This function upload chunk(of lines) from each file(postinglist
#         :return:
#         """
#         for i in range(len(self.filesNames)):
#             self.chunksListToMerge.append(0)
#             self.pointers.append(0)
#             self.uploadFileChunk(i)
#
#     def uploadFileChunk(self, fileNumber):
#
#         termDict = self.readlines(fileNumber, self.pointers[fileNumber], self.chunkSize)
#         self.chunksListToMerge[fileNumber] = termDict
#
#     def readlines(self, fileNumber, start, howManyToRead):
#         """
#         This function read specific lines from a file.
#         :param fileName: the name of file to read from
#         :param start: from which line start to read
#         :param howManyToRead:
#         :return: dictionary
#         """
#         fileName = self.filesToMergePath + '/' + self.filesNames[fileNumber]
#         keys = []
#         values = []
#         if start < 0: return ''
#         current_line_number = 0
#         eof=True
#         for line in open(fileName):
#             if start <= current_line_number < start + howManyToRead:
#                 tmp = line.split(':')
#                 keys.append(tmp[0])
#                 values.append(tmp[1].replace('\n', ''))
#                 eof=False
#             current_line_number += 1
#             if current_line_number == start + howManyToRead:
#                 break
#         if eof:
#             self.pointers[fileNumber] = -1
#             return [[""], [""]]
#         if current_line_number != start + howManyToRead:
#             for i in range(0,howManyToRead+start-current_line_number):
#                 keys.insert(0,"")
#                 values.insert(0,"")
#             self.pointers[fileNumber]=howManyToRead+start-(current_line_number%howManyToRead)
#
#
#         return [keys, values]
#
#     def findMin(self, terms):
#         """
#         This function find the minimum value in list
#         :param terms: list of terms
#         :return: the index of minimum value
#         """
#         min = 0
#         i = 0
#         while self.pointers[min]==-1:
#             min+=1
#         while i < len(terms):
#             if self.pointers[i] != -1:
#                 if terms[i] < terms[min]:
#                     min = i
#             i += 1
#         return min
#
#     def hasFinished(self):
#
#         ans = True
#         for i in range(len(self.pointers)):
#             if self.pointers[i] != -1:
#                 ans = False
#                 break
#         return ans
#
#     def writeMergeContentToDisk(self,fileName):
#         """
#         This function writes the posting list into the disc
#         :return:
#         """
#         with open(fileName, "a+",-1,"utf-8") as out:
#             for key in self.postingBlock.keys():
#                 out.write(key + ":")
#                 out.write(self.postingBlock[key] + '\n')
#         out.close()
#         self.postingBlock = {}
#
#     def writeDictionaryToDisk(self):
#         """
#         This function writes the dictionary into the disc
#         :return:
#         """
#         with open("dictionary.txt", "a+") as out:
#             for key in self.dictionary.keys():
#                 out.write(key + ":")
#                 out.write(self.dictionary[key].toString() + '\n')
#         out.close()
#
#     def AddToDictionary(self, term, postingListPointer):
#
#         e=DictionaryElement("")
#         if term=="" or str(term)[0].isupper():
#             if self.dictionary.__contains__(term.lower()):
#                 self.dictionary[term.upper()].pointer *= -1
#
#             elif self.postingBlock.keys().__contains__(str(term).upper()):
#                 self.postingBlock[term.upper()]+=self.postingBlock[term]
#             else:
#                 term = term.upper()
#                 e.pointer=postingListPointer
#                 self.dictionary[term] = e
#         else:
#             if term.islower() and self.dictionary.__contains__(term.upper()):
#                 self.dictionary[term.upper()].pointer *= -1
#             e.pointer = postingListPointer
#             self.dictionary[term] = e
#
#     def clearUpperCase(self):
#         """
#         This function responsible to merge term that appear multiple times in dictionary in different forms,
#         for example: one time in uppercase and another time with lowercase.
#         After the merge, it updates the new pointers for each term in dictionary
#         :return:
#         """
#         postingBlock = {}
#         keys_to_delete=[]
#         for key in self.dictionary.keys():
#
#             if self.dictionary[key].pointer < 0:
#                 pointer = self.dictionary[key].pointer * (-1)
#                 # oldPosting.seek(pointer)
#                 linec=linecache.getline("postingTmp.txt",pointer)
#                 # print(linec.split(':')[0])
#                 # if key.lower() != linec.split(':')[0].lower():
#                 #     print(key)
#
#                 # print(oldPosting.readline())
#                 upperLine = linec.split(':')[1]
#
#                 #get the posting list of the term in lowercase
#                 # oldPosting.seek(self.dictionary[key.lower()].pointer)
#                 lowerLine = linecache.getline("postingTmp.txt",self.dictionary[key.lower()].pointer).replace('\n','')
#                 lowerLine += " "+upperLine
#                 # print(lowerLine)
#                 tmp=lowerLine.split(':')
#                 postingBlock[tmp[0]]=tmp[1]
#                 keys_to_delete.append(key)
#
#         for key in keys_to_delete:
#             del self.dictionary[key]
#         with open("key.txt","w+") as k:
#             for key in keys_to_delete:
#                 k.write(key+'\n')
#         with open("posting.txt", "w+") as newPosting:
#             i = 0
#             line_num=1
#             continu=0
#             pos_keys=postingBlock.keys()
#             print("dict----------"+str(len(self.dictionary.keys())))
#             print("delete--------"+str(len(pos_keys)))
#             j=0
#             while j <len(self.dictionary.keys()):
#                 line = linecache.getline("postingTmp.txt",line_num)
#                 if line=="":
#                     break
#                 tmp=line.split(':')[0]
#                 if tmp=="" or tmp[0].isupper():
#                     key=tmp.upper()
#                 elif tmp[0].islower():
#                     key = tmp.lower()
#                 else:
#                     key=tmp
#                 if key not in self.dictionary.keys():
#                     line_num+=1
#                     continu+=1
#                     continue
#
#                 if key in pos_keys:
#                     line= key +":"+postingBlock[key]
#
#                 newPosting.write(line)
#                 # print(j)
#                 self.dictionary[key].pointer=i
#                 self.dictionary[key].corpus_tf=self.calculateTotalTf(line)
#                 i += len(line)+1
#                 line_num+=1
#                 j+=1
#         print(continu)
#         newPosting.close()
#         # os.remove("postingTmp.txt")
#
#     def calculateTotalTf(self, line):
#
#         term_corpus_frequency = 0
#         try:
#              tmp=line.split(':')
#              posting=tmp[1]
#
#              elements=posting.split()
#              for i in range(len(elements)):
#                  term_corpus_frequency+=int(str(elements[i].split(',')[1]))
#         except:
#             print(line)
#         return term_corpus_frequency
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
