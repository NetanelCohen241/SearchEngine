import os
import linecache

class DictionaryElement(object):

    def __init__(self,postingFile):
        self.postingFile=postingFile
        self.corpus_tf=0
        self.pointer=0

    def toString(self):
        return self.postingFile+","+str(self.pointer)+","+str(self.corpus_tf)


class Merger(object):

    def __init__(self, filesToMergePath, chunkSize):

        self.filesToMergePath = filesToMergePath
        self.chunkSize = chunkSize
        self.dictionary = {}
        self.postingBlock = {}
        self.chunksListToMerge = []
        self.filesNames = [word for word in os.listdir(self.filesToMergePath) if word.startswith("posting")]
        self.pointers = []
        open("postingTmp.txt", "w+")
        open("dictionary.txt", "w+")

    def merge(self):
        """
        This function merge the files into one sorted file - posting list
        :return:
        """

        terms = []
        self.uploadAllFilesChunks()
        # insert into terms list the first term from each chunk
        for i in range(0, len(self.chunksListToMerge)):
            terms.append(self.chunksListToMerge[i][0][self.pointers[i]])

        self.startMerge(terms)
        self.writeMergeContentToDisk("postingTmp.txt")
        # self.writeDictionaryToDisk()
        print("merge is done")
        # self.updatePointers()
        self.clearUpperCase()
        self.writeDictionaryToDisk()

    def startMerge(self, terms):
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
        postingListPointer = 1
        while not self.hasFinished():

            minTermIdx = self.findMin(terms)
            term = self.chunksListToMerge[minTermIdx][0][self.pointers[minTermIdx] % self.chunkSize]

            self.postingBlock[term] = ""
            # iterate over each chunk, in every chunk that the term exists, append its content to postingBlock
            for i in range(0, len(self.chunksListToMerge)):
                # check if we already uploaded the all file
                if self.pointers[i] == -1:
                    continue
                pos = self.pointers[i] % self.chunkSize
                if self.chunksListToMerge[i][0][pos] == term:
                    #append term content to posting list
                    self.postingBlock[term] += self.chunksListToMerge[i][1][pos]
                    self.pointers[i] += 1
                    if self.pointers[i] % self.chunkSize == 0:
                        self.uploadFileChunk(i)
                    if self.pointers[i] != -1:
                        terms[i] = self.chunksListToMerge[i][0][self.pointers[i] % self.chunkSize]


            self.AddToDictionary(term, postingListPointer)

            postingListPointer += 1
            # if postingListPointer % 500000 == 0:
            #     self.writeMergeContentToDisk("postingTmp.txt")

    def uploadAllFilesChunks(self):
        """
        This function upload chunk(of lines) from each file(postinglist
        :return:
        """
        for i in range(len(self.filesNames)):
            self.chunksListToMerge.append(0)
            self.pointers.append(0)
            self.uploadFileChunk(i)

    def uploadFileChunk(self, fileNumber):

        termDict = self.readlines(fileNumber, self.pointers[fileNumber], self.chunkSize)
        self.chunksListToMerge[fileNumber] = termDict

    def readlines(self, fileNumber, start, howManyToRead):
        """
        This function read specific lines from a file.
        :param fileName: the name of file to read from
        :param start: from which line start to read
        :param howManyToRead:
        :return: dictionary
        """
        fileName = self.filesToMergePath + '/' + self.filesNames[fileNumber]
        keys = []
        values = []
        if start < 0: return ''
        current_line_number = 0
        eof=True
        for line in open(fileName):
            if start <= current_line_number < start + howManyToRead:
                tmp = line.split(':')
                keys.append(tmp[0])
                values.append(tmp[1].replace('\n', ''))
                eof=False
            current_line_number += 1
            if current_line_number == start + howManyToRead:
                break
        if eof:
            self.pointers[fileNumber] = -1
            return [[""], [""]]
        if current_line_number != start + howManyToRead:
            for i in range(0,howManyToRead+start-current_line_number):
                keys.insert(0,"")
                values.insert(0,"")
            self.pointers[fileNumber]=howManyToRead+start-(current_line_number%howManyToRead)


        return [keys, values]

    def findMin(self, terms):
        """
        This function find the minimum value in list
        :param terms: list of terms
        :return: the index of minimum value
        """
        min = 0
        i = 0
        while self.pointers[min]==-1:
            min+=1
        while i < len(terms):
            if self.pointers[i] != -1:
                if terms[i] < terms[min]:
                    min = i
            i += 1
        return min

    def hasFinished(self):

        ans = True
        for i in range(len(self.pointers)):
            if self.pointers[i] != -1:
                ans = False
                break
        return ans

    def writeMergeContentToDisk(self,fileName):
        """
        This function writes the posting list into the disc
        :return:
        """
        with open(fileName, "a+",-1,"utf-8") as out:
            for key in self.postingBlock.keys():
                out.write(key + ":")
                out.write(self.postingBlock[key] + '\n')
        out.close()
        self.postingBlock = {}

    def writeDictionaryToDisk(self):
        """
        This function writes the dictionary into the disc
        :return:
        """
        with open("dictionary.txt", "a+") as out:
            for key in self.dictionary.keys():
                out.write(key + ":")
                out.write(self.dictionary[key].toString() + '\n')
        out.close()

    def AddToDictionary(self, term, postingListPointer):

        e=DictionaryElement("")
        if term=="" or str(term)[0].isupper():
            if self.dictionary.__contains__(term.lower()):
                self.dictionary[term.upper()].pointer *= -1
            # elif self.postingBlock.keys().__contains__(str(term).upper()):
            #     self.postingBlock[term.upper()]+=self.postingBlock[term]
            else:
                term = term.upper()
                e.pointer=postingListPointer
                self.dictionary[term] = e
        else:
            if term.islower() and self.dictionary.__contains__(term.upper()):
                self.dictionary[term.upper()].pointer *= -1
            e.pointer = postingListPointer
            self.dictionary[term] = e

    def clearUpperCase(self):
        """
        This function responsible to merge term that appear multiple times in dictionary in different forms,
        for example: one time in uppercase and another time with lowercase.
        After the merge, it update the new pointers for each term in dictionary
        :return:
        """
        with open("postingTmp.txt", "r") as oldPosting:
            postingBlock = {}
            i=0
            keys_to_delete=[]
            for key in self.dictionary.keys():

                if self.dictionary[key].pointer < 0:
                    pointer = self.dictionary[key].pointer * (-1)
                    # oldPosting.seek(pointer)
                    linec=linecache.getline("postingTmp.txt",pointer)
                    # print(linec.split(':')[0])
                    if key.lower() != linec.split(':')[0].lower():
                        print(key)

                    # print(oldPosting.readline())
                    upperLine = linec.split(':')[1]

                    #get the posting list of the term in lowercase
                    # oldPosting.seek(self.dictionary[key.lower()].pointer)
                    lowerLine = linecache.getline("postingTmp.txt",self.dictionary[key.lower()].pointer).replace('\n','')
                    lowerLine += " "+upperLine
                    # print(lowerLine)
                    tmp=lowerLine.split(':')
                    postingBlock[tmp[0]]=tmp[1]
                    keys_to_delete.append(key)

                i+=1
            for key in keys_to_delete:
                del self.dictionary[key]
            print(len(keys_to_delete))
            print(len(self.dictionary.keys()))
            with open("posting.txt", "w+") as newPosting:
                i = 0
                line_num=1
                pos_keys=postingBlock.keys()
                for key in self.dictionary.keys():
                    line = linecache.getline("postingTmp.txt",line_num)
                    tmp=line.split(':')
                    if tmp[0] not in self.dictionary.keys():
                        line_num+=1
                        continue
                    if tmp[0] in pos_keys:
                        line= key +":"+postingBlock[tmp[0]]

                    newPosting.write(line)
                    self.dictionary[key].pointer=i
                    self.dictionary[key].corpus_tf=self.calculateTotalTf(line)
                    i += len(line)
                    line_num+=1
            newPosting.close()
        oldPosting.close()
        # os.remove("postingTmp.txt")

    def calculateTotalTf(self, line):

        term_corpus_frequency = 0
        try:
             tmp=line.split(':')
             posting=tmp[1]

             elements=posting.split()
             for i in range(len(elements)):
                 term_corpus_frequency+=int(str(elements[i].split(',')[1]))
        except:
            print(line)
        return term_corpus_frequency

