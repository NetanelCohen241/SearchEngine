import Reader
import Parse

class postingElement(object):

    def __init__(self, docNo, tf):
        self.docNo=docNo
        self.tf=tf

    def updateTf(self,tf):
        self.tf=tf

    def toString(self):
        return self.docNo+","+str(self.tf)

class index(object):

    def __init__(self,corpusPath,postingListPath):
        self.corpusPath=corpusPath
        self.postingListPath=postingListPath
        self.postingList={}

    def createIndex(self,withStemming,pid):

        blockSize=2
        read=Reader.ReadFile(self.corpusPath)
        parser=Parse.Parser()
        docList=read.startAction(pid*blockSize,blockSize)
        for doc in docList:
            terms=parser.parse(doc.txt,withStemming)
            docDictionary = {}
            for i in range(len(terms)):

                if docDictionary.__contains__(terms[i]):
                    docDictionary[terms[i]]+=1
                else:
                    docDictionary[terms[i]]=1

            self.insertToPostingList(docDictionary,doc)

        self.writePostingListToDisk(pid)


    def insertToPostingList(self, docDictionary,doc):

        # for key, value in transaction.items():
        for key in docDictionary.keys():
            value=docDictionary[key]
            if self.postingList.__contains__(key):
                self.postingList[key].append(postingElement(doc.docNumber, value))
            else:
                self.postingList[key] = []
                self.postingList[key].append(postingElement(doc.docNumber, value))

    def writePostingListToDisk(self, pid):

        with open(self.postingListPath +'/' +"test" + str(pid) + ".txt", "w+") as out:

            for key in sorted(self.postingList.keys()):
                out.write(key+ " : ")
                for element in self.postingList[key]:
                    out.write(element.toString()+ " " )
                out.write("\n")
        out.close()






