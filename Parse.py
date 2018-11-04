import nltk
import re
months = ["january", "jan", "february", "feb", "march", "mar", "april", "apr", "may", "june", "jun", "july", "jul",
          "august", "aug", "september", "sep", "october", "oct", "november", "nov", "december", "dec"]


class Parser:

    def __init__(self):

        self.terms=[]


    def parse(self,text):
        i=0
        terms=[]
        tokens=nltk.word_tokenize(text)
        while i < len(tokens):

            if tokens[i].isdigit():
                # Date
                mon= self.getMonth(tokens[i+1].lower())
                if mon!=0:
                    terms.append(self.dateFormat(mon, tokens[i]))
                    i = i + 1
            # Number
            elif self.isNumber(tokens[i]):

                #Percent
                if tokens[i+1] is "percent" or tokens[i+1] is "percentage" or tokens[i+1] is "%":
                    term=tokens[i+1]+"%"
                #Price
                elif tokens[i+1] is "Dollars" or tokens[i+2] is "Dollars" or tokens[i+3] is "dollars":
                    i,term=self.calcPrice(tokens,i)
                #Number(only size)
                else:
                    i,term=self.calcSize(tokens,i)


            elif tokens[i] == '$':
                if self.isNumber(tokens[i+1]):
                    i, term = self.calcPrice(tokens, i)

            #Word
            else:
                #Date
                mon = self.getMonth(tokens[i].lower())
                if mon != 0:
                    if tokens[i + 1].isdigit():
                        term=self.dateFormat(mon, tokens[i+1])
                        i=i+1
                    else:
                        term=tokens[i]

                #check if its the range pattern: "between Number and Number"
                elif tokens[i].lower() is "between" and self.isNumber(tokens[i+1]) and tokens[i+2].lower() is "and" and self.isNumber(tokens[i+3]):
                    term="between "+tokens[i+1]+" and "+tokens[i+3]
                    i=i+3

            terms.append(term)
            i=i+1


    #TODO:Twitoo
    def calcSize(self,tokens,i):
        term=""
        return i,term



    #get num of month and day, return date format MM-DD or YYYY-MM
    def dateFormat(self, month, number):

        if(number<10):
            number= "0"+number
        if number>31:
            return number + "-" + month
        else:
            return month + "-" + number

    #param- name of month
    #return the month number or  if its not a month
    def getMonth(self, month):

        for i in len(24):
            if month == months[i]:
                if i < 12:
                    return "0"+i/2
                else:
                    return ""+i/2

        return ""+0

    #param- token
    #return true if its a number or fraction
    def isNumber(self, token):

        #1st- regular expression that detect number like X,YYY  or X,YYY.ZZ
        return re.match("^(\d+|\d{1,3}(,\d{3})*)(\.\d+)?$",token) or self.isFraction(token)

    def isFraction(self, token):
        # regular expression that can detect fraction from the pattern X/Y
        return re.match("([1-9]\/[1-9])", token)

    #return price term according price term rules
    def calcPrice(self, tokens, i):

        term=""
        # term= ""+self.calcPriceValue()


        return i,term






