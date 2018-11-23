import os
import linecache


class Merger(object):

    def __init__(self, filesToMergePath,chunkSize):

        self.filesToMergePath = filesToMergePath
        self.chunkSize = chunkSize
        self.dictionary = {}
        self.postingBlock = {}
        self.chunksListToMerge = []
        self.filesNames = os.listdir(self.filesToMergePath)
        self.pointers = []

    def merge(self):
        """
        This function merge the files into one sorted file-posting list
        :return:
        """

        terms = []
        self.uploadAllFilesChunks()
        #insert into terms list the first term from each chunk
        for i in range(0, len(self.chunksListToMerge)):
            terms.append(self.chunksListToMerge[i][0][self.pointers[i]])

        self.startMerge(terms)
        self.writeMergeContentToDisk()



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
        while not self.hasFinished():

            minTermIdx = self.findMin(terms)
            term = self.chunksListToMerge[minTermIdx][0][self.pointers[minTermIdx]]
            self.dictionary[term] = minTermIdx
            self.postingBlock[term] = ""
            #iterate over each chunk, in every chunk that the term exists, append its content to postingBlock
            for i in range(0, len(self.chunksListToMerge)):
                #check if we already uploaded the all file
                if self.pointers[i]==-1:
                    continue
                if self.chunksListToMerge[i][0][self.pointers[i]] == term:
                    self.postingBlock[term] += self.chunksListToMerge[i][1][self.pointers[i]]
                    self.pointers[i] += 1
                    if self.pointers[i] % self.chunkSize == 0:
                        self.uploadFileChunk(i)
                    terms[i] = self.chunksListToMerge[i][0][self.pointers[i]]


    #this function can be multi-threaded
    def uploadAllFilesChunks(self):

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
        line=""
        for i in range(start, howManyToRead):
            try:
                line = linecache.getline(fileName, i+1)
            except:
                print (fileName)
                print(i+1)
            if line == "":
                self.pointers[fileNumber]=-1
            tmp = line.split(':')
            try:
                keys.append(tmp[0])
                values.append(tmp[1])
            except:
                print(line)

        return [keys, values]

    def findMin(self, terms):
        """
        This function find the minimum value in list
        :param terms: list of terms
        :return: the index of minimum value
        """
        min = terms[0]
        i = 0
        while i < len(terms):
            if (terms[i] < min):
                min = terms[i]
        return i

    def hasFinished(self):

        ans = True
        for i in range(len(self.pointers)):
            if self.pointers[i]!=-1:
                ans= False
                break
        return ans

    def writeMergeContentToDisk(self):

        with open(self.filesToMergePath +'/' +"mergedContent" + ".txt", "w+") as out:

            for key in self.postingBlock.keys():
                out.write(key+ ":")
                out.write(self.postingBlock[key])
        out.close()

        with open(self.filesToMergePath +'/' +"dictionary" + ".txt", "w+") as out:

            for key in self.postingBlock.keys():
                out.write(key+ ":")
                out.write(self.postingBlock[key])
        out.close()

