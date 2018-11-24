class Document:
    def __init__(self,docNumber,txt,city=""):
        self.docNumber=docNumber
        self.txt=txt
        self.city=city

    def toString(self):
        return "Number: {0}\nCity: {1}\n Text: {2}".format(self.docNumber,self.city,self.txt)

