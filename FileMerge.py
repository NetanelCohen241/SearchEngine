import os
import linecache


class Merger(object):

    def __init__(self, filesToMergePath, chunkSize):

        self.filesToMergePath = filesToMergePath
        self.chunkSize = chunkSize
        self.dictionary = {}
        self.postingBlock = {}
        self.chunksListToMerge = []
        self.filesNames = os.listdir(self.filesToMergePath)
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
            try:
                term = self.chunksListToMerge[minTermIdx][0][self.pointers[minTermIdx] % self.chunkSize]
            except:
                print(self.pointers)
                # print( self.chunksListToMerge[minTermIdx][0])
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
            if postingListPointer % 100000 == 0:
                self.writeMergeContentToDisk("postingTmp.txt")

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
        for line in open(fileName):
            if current_line_number >= start:
                tmp = line.split(':')
                keys.append(tmp[0])
                values.append(tmp[1].replace('\n', ''))
            current_line_number += 1
            if current_line_number == start + howManyToRead:
                break
        if current_line_number != start + howManyToRead:
            self.pointers[fileNumber] = -1
        return [keys, values]

    def findMin(self, terms):
        """
        This function find the minimum value in list
        :param terms: list of terms
        :return: the index of minimum value
        """
        min = 0
        i = 0
        while i < len(terms):
            if self.pointers[i] != -1 and terms[i] < terms[min]:
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
        with open(fileName, "a+") as out:
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
                out.write(key + " : ")
                out.write(str(self.dictionary[key]) + '\n')
        out.close()

    def AddToDictionary(self, term, postingListPointer):

        if term=="" or str(term)[0].isupper():
            if self.dictionary.__contains__(term.lower()):
                # self.postingBlock[term.lower()]+= self.postingBlock[term]
                self.dictionary[term.upper()] *= -1
            else:
                term = term.upper()
                self.dictionary[term] = postingListPointer
        else:
            if term.islower() and self.dictionary.__contains__(term.upper()):
                self.dictionary[term.upper()] *= -1
            else:
                self.dictionary[term] = postingListPointer

    def clearUpperCase(self):
        """
        This function responsible to merge term that appear multiple times in dictionary in different forms,
        for example: one time in uppercase and another time with lowercase.
        After the merge, it update the new pointers for each term in dictionary
        :return:
        """
        postingBlock = {}
        for key in self.dictionary:
            if self.dictionary[key] < 0:
                pointer = self.dictionary[key] * (-1)
                upperLine = linecache.getline("postingTmp.txt", pointer).split(':')[1]
                lowerLine = linecache.getline("postingTmp.txt", self.dictionary[key.lower()])
                lowerLine += upperLine.replace('\n','')
                tmp=lowerLine.split(':')
                postingBlock[tmp[0]]=tmp[1]
                del self.dictionary[key]

        with open("posting.txt", "w+") as out:
            i = 1
            keys=postingBlock.keys()
            for key in self.dictionary:
                line = linecache.getline("postingTmp.txt", i)
                if line.split(':')[0] in keys:
                    line= key +":"+postingBlock[key]
                out.write(line)
                self.dictionary[key]=i
                i += 1
        out.close()
        os.remove("postingTmp.txt")