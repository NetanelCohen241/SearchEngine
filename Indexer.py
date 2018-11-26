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
        # self.docs=[]

    def createIndex(self,withStemming,pid):
        """
        This function creates an inverted index.
        :param withStemming: determines whether do stemming or not
        :param pid: number of chunk to read.
        :return: a dictionary: key=term, value= how many the term appeared in the doc(tf)
        """
        postingList = {}
        blockSize=40
        read=Reader.ReadFile(self.corpusPath)
        parser=Parse.Parser()
        docList=read.startAction(pid*blockSize,blockSize)

        for doc in docList:
            docDictionary=parser.parse(doc.txt,withStemming)
            doc.setNumOfUniqeTerms(len(docDictionary.keys()))
            doc.setMaxtf(self.calcMaxTf(docDictionary))
            self.insertToPostingList(postingList,docDictionary,doc)
        self.writeDocsToDick(docList,pid)
        self.writePostingListToDisk(postingList,pid)


    def insertToPostingList(self, postingList, docDictionary,doc):

        for key in docDictionary.keys():
            value=docDictionary[key]
            if postingList.__contains__(key):
                postingList[key].append(PostingElement(doc.docNumber, value))
            else:
                postingList[key] = []
                postingList[key].append(PostingElement(doc.docNumber, value))

    def writePostingListToDisk(self, postingList, pid):

        with open(self.postingListPath +'/' +"posting" + str(pid) + ".txt", "w+") as out:

            for key in sorted(postingList.keys()):
                out.write(key+ ":")
                for element in postingList[key]:
                    out.write(element.toString()+ " " )
                out.write("\n")
        out.close()

    def calcMaxTf(self, docDictionary):

        keys=docDictionary.keys()
        max=0
        for key in keys:
            if docDictionary[key]> max:
                max=docDictionary[key]

        return max

    def writeDocsToDick(self, docList,pid):

        with open(self.postingListPath +'/' +"docs" + str(pid) + ".txt", "w+") as out:
            out.write("Number            City            CityLocations             NumOfUniqeTerms    maxTf\n")
            for doc in docList:
                out.write(doc.toString()+"\n")
        out.close()








