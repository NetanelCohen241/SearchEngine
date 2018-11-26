class Document:
    def __init__(self,docNumber,txt,city=""):
        self.docNumber=docNumber
        self.txt=txt
        self.city=city
        self.cityLocations=[]
        self.numOfUniqeTerms=0
        self.maxTf=0

    def setMaxtf(self,max_tf):
        self.maxTf=max_tf

    def setNumOfUniqeTerms(self, numOfUniqeTerms):
        self.numOfUniqeTerms=numOfUniqeTerms

    def toString(self):
        return "{0}            {1}            {2}             {3}    {4}"\
                .format(self.docNumber,self.city,self.cityLocations,self.numOfUniqeTerms ,self.maxTf)

