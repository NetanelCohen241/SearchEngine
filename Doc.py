class Document:
    def __init__(self,docNumber,txt,city=""):
        self.docNumber=docNumber
        self.txt=txt
        self.city=city
        self.cityLocations=[]
        self.numOfUniqeTerms=0
        self.maxTf=0
        self.data_of_publish=""
        self.title=""
        #data of publish
        #title

    def setMaxtf(self,max_tf):
        self.maxTf=max_tf

    def setNumOfUniqeTerms(self, numOfUniqeTerms):
        self.numOfUniqeTerms=numOfUniqeTerms

    def setTitle(self,title):
        self.title=title

    def setDate(self,date):
        self.data_of_publish=date

    def toString(self):
        return "{0}            {1}            {2}             {3}            {4}         {5}         {6}"\
                .format(self.docNumber,self.city,self.cityLocations,self.numOfUniqeTerms ,self.maxTf,self.title,self.data_of_publish)

