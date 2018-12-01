import Reader
import Parse

class PostingElement(object):

    def __init__(self, docNo, tf, inTitle):
        self.docNo=docNo
        self.tf=tf
        self.inTitle=inTitle

    def updateTf(self,tf):
        self.tf=tf

    def toString(self):
        return self.docNo.replace(" ",'')+","+str(self.tf.toString())+","+str(self.inTitle)


class City(object):
    def __init__(self):
        self.currency=""
        self.population=""
        self.name=""

    def toString(self):
        return "{0}            {1}            {2}" \
            .format(self.name, self.currency, self.population)


class Index(object):

    def __init__(self,corpusPath,postingListPath,city_dict):
        self.corpusPath=corpusPath
        self.postingListPath=postingListPath
        self.city_dict_from_api=city_dict
        self.parser = Parse.Parser()
        # self.docs=[]

    def createIndex(self,withStemming,pid):
        """
        This function creates an inverted index.
        :param withStemming: determines whether do stemming or not
        :param pid: number of chunk to read.
        :return: a dictionary: key=term, value= how many the term appeared in the doc(tf)
        """
        postingList = {}
        ##create city dict{} key=city value=obj with relevent data api data + list docs
        city = {}
        blockSize=40
        read=Reader.ReadFile(self.corpusPath)
        docList=read.startAction(pid*blockSize,blockSize)

        for doc in docList:
            docDictionary=self.parser.parse(doc.txt,withStemming)
            doc.title=self.parser.parse(" ".join(doc.title),withStemming).keys()
            doc.setNumOfUniqeTerms(len(docDictionary.keys()))
            doc.setMaxtf(self.calcMaxTf(docDictionary))
            self.insertToPostingList(postingList,docDictionary,doc)
            self.insert_to_city(city,doc)
        self.writeCityToDisk(city,pid)
        self.writeDocsToDisk(docList,pid)
        self.writePostingListToDisk(postingList,pid)


    def insertToPostingList(self, postingList, docDictionary,doc):
        """

        :param postingList:
        :param docDictionary:
        :param doc:
        :return:
        """
        for key in docDictionary.keys():
            inTitle="F"
            value=docDictionary[key]
            if key in doc.title:
                inTitle="T"
            if postingList.__contains__(key):
                postingList[key].append(PostingElement(doc.docNumber, value, inTitle))
            else:
                postingList[key] = []
                postingList[key].append(PostingElement(doc.docNumber, value, inTitle))

    def insert_to_city(self, my_city, doc):
        if doc.city=="" or doc.city==[]:
            return
        doc_city=doc.city.lower()
        if doc_city in my_city.keys():
            return
        city_obj = City()
        if doc_city in self.city_dict_from_api:
             data = self.city_dict_from_api[doc_city]
             city_obj.name = data[0]
             city_obj.currency = data[1]
             trash,city_obj.population = self.parser.calcSize([data[2]], 0)
        else:
            city_obj.name = "N"
            city_obj.currency = "N"
            city_obj.population = "0"
            my_city[doc_city] = city_obj


    def writePostingListToDisk(self, postingList, pid):
        """
        This function sorts the posting list and writes it into the disk.
        :param postingList: given posting list
        :param pid:
        :return:
        """
        with open(self.postingListPath +'/' +"posting" + str(pid) + ".txt", "w+") as out:

            for key in sorted(postingList.keys()):
                out.write(key+ ":")
                for element in postingList[key]:
                    out.write(element.toString()+ " ")
                out.write("\n")
        out.close()

    def calcMaxTf(self, docDictionary):

        keys=docDictionary.keys()
        max=0
        for key in keys:
            if docDictionary[key].frq> max:
                max=docDictionary[key].frq

        return max

    def writeDocsToDisk(self, docList,pid):

        with open("docs.txt", "a") as out:
            for doc in docList:
                out.write(doc.toString()+"\n")
        out.close()

    ##write city to disc
    def writeCityToDisk(self, city, pid):
        if city.keys() == []:
            return
        with open(self.postingListPath +'/' +"city" + str(pid) + ".txt", "w+") as out:

            for key in sorted(city.keys()):
                out.write(key+ ":           "+city[key].toString()+ " " )
                out.write("\n")
        out.close()







