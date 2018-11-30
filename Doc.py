class Document:
    def __init__(self,docNumber,txt,city=""):
        self.docNumber=docNumber
        self.txt=txt
        self.city=city
        self.cityLocations=[]
        self.numOfUniqeTerms=0
        self.maxTf=0
        self.date_of_publish= ""
        self.title=""

    def setMaxtf(self,max_tf):
        self.maxTf=max_tf

    def setNumOfUniqeTerms(self, numOfUniqeTerms):
        self.numOfUniqeTerms=numOfUniqeTerms

    def setTitle(self,title):
        self.title=title

    def setDate(self,date):
        self.date_of_publish=date

    def toString(self):
        return "{0}            {1}            {2}             {3}            {4}         {5}         {6}"\
                .format(self.docNumber, self.city, self.cityLocations, self.numOfUniqeTerms, self.maxTf, self.date_of_publish, self.title)

