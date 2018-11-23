import Reader
import Parse

class PostingElement(object):

    def __init__(self, docNo, tf):
        self.docNo=docNo
        self.tf=tf

    def updateTf(self,tf):
        self.tf=tf

    def toString(self):
        return self.docNo+","+str(self.tf)

class Index(object):

    def __init__(self,corpusPath,postingListPath):
        self.corpusPath=corpusPath
        self.postingListPath=postingListPath

    def createIndex(self,withStemming,pid):

        postingList = {}
        blockSize=50
        read=Reader.ReadFile(self.corpusPath)
        parser=Parse.Parser()
        docList=read.startAction(pid*blockSize,blockSize)

        for doc in docList:
            docDictionary=parser.parse(doc.txt,withStemming)
            self.insertToPostingList(postingList,docDictionary,doc)

        self.writePostingListToDisk(postingList,pid)


    def insertToPostingList(self, postingList, docDictionary,doc):

        # for key, value in transaction.items():
        for key in docDictionary.keys():
            value=docDictionary[key]
            if postingList.__contains__(key):
                postingList[key].append(PostingElement(doc.docNumber, value))
            else:
                postingList[key] = []
                postingList[key].append(PostingElement(doc.docNumber, value))

    def writePostingListToDisk(self, postingList, pid):

        with open(self.postingListPath +'/' +"test" + str(pid) + ".txt", "w+") as out:

            for key in sorted(postingList.keys()):
                out.write(key+ ":")
                for element in postingList[key]:
                    out.write(element.toString()+ " " )
                out.write("\n")
        out.close()






