class Document:
    def __init__(self,docNumber,txt,city=""):
        self.docNumber=docNumber
        self.txt=txt
        self.city=city
        self.city_locations=[]
        self.num_of_unique_terms=0
        self.max_tf=0
        self.date_of_publish= ""
        self.title=[]
        self.language=""

    def set_maxtf(self, max_tf):
        self.max_tf=max_tf

    def set_num_of_uniqe_terms(self, numOfUniqeTerms):
        self.num_of_unique_terms=numOfUniqeTerms

    def set_title(self, title):
        self.title=title

    def set_date(self, date):
        self.date_of_publish=date

    def set_language(self, lan):
        self.language = lan


    def to_string(self):
        return "{0}            {1}            {2}             {3}            {4}"\
                .format(self.docNumber, self.city if self.city != "" else "----", self.num_of_unique_terms, self.max_tf, self.date_of_publish)

