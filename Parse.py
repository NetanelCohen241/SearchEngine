import ast
import nltk
import re
from nltk.stem import PorterStemmer


months = ["january", "jan", "february", "feb", "march", "mar", "april", "apr", "may", "may", "june", "jun", "july", "jul",
          "august", "aug", "september", "sep", "october", "oct", "november", "nov", "december", "dec"]

size = ["trillion", "billion", "million", "thousand"]
class Parser:

    def __init__(self):

        self.terms=[]


    def parse(self,text,withStemming):
        i=0
        terms=[]

        tokens= (str(text).replace(':','').replace('"','').replace('!','').replace('?','').replace('*','')
                 .replace('(','').replace(')','').replace('[','').replace(']','').replace('{','').replace('}','').split(' '))
        with open("stop_words.txt","r") as sw:
            stopWords=sw.read();
        while i < len(tokens):
            term = ""
            if tokens[i] in stopWords:
                i=i+1
                continue
            #Price
            if tokens[i].startswith("$",0,1):
                tokens[i]=tokens[i].replace('$', '')
                if '-' in tokens[i]:
                    j, term = self.calcPrice(tokens[i].replace('-',' ').split(' '), 0, True)
                elif i+1<len(tokens):
                    j, term = self.calcPrice([tokens[i],tokens[i+1]], 0, True)
                    i+=j
                else:
                    j, term = self.calcPrice(tokens[i], 0, True)


            #Percent
            elif tokens[i].endswith("%",len(tokens[i])-1):
                tokens[i]=tokens[i].replace('%', '')
                if self.isNumber(tokens[i]):
                    i,term= self.calcSize(tokens,i)
                    term+="%"
            # Number
            elif self.isNumber(tokens[i]):

                #Percent
                if i+1<len(tokens) and (tokens[i+1] == "percent" or tokens[i+1] == "percentage"):
                    i, term = self.calcSize(tokens, i)
                    term += '%'
                    i=i+1
                #Price
                elif (i+1<len(tokens) and tokens[i+1] == "Dollars") or (i+2<len(tokens) and (tokens[i+2] == "Dollars" or tokens[i+2] == "U.S.")):
                    i,term= self.calcPrice(tokens, i, False)
                #Number(only size)
                else:
                    acc=0
                    #number range
                    if i+1<len(tokens) and '-' in tokens[i+1]:
                        rangeTokens=tokens[i+1].split('-')
                        if rangeTokens[0].lower() in size:
                            #left value in range
                            j,t=self.calcSize([tokens[i],rangeTokens[0]],0)
                            terms.append(t)
                            term=t
                            acc=acc+1
                            if self.isNumber(rangeTokens[1]):
                                # Number-Number
                                if i+2<len(tokens) and tokens[i+2].lower() in size:
                                    j, t2 = self.calcSize([rangeTokens[1], tokens[i+2]], 0)
                                    terms.append(t2)
                                    term=term+"-"+t2
                                    i=i+acc+1
                            #Number-Word
                            else:
                                i=i+1
                                term=term+"-"+rangeTokens[1]
                    elif tokens[i].isdigit():
                        # Date
                        if i+1<len(tokens):
                            mon = self.getMonth(tokens[i+1].lower())
                            if mon is not "0":
                                term = self.dateFormat(mon, tokens[i])
                                i=i+1
                            else:
                                i,term=self.calcSize(tokens,i)
                    else:
                        i, term = self.calcSize(tokens, i)

            #Word
            else:
                #Date
                mon = self.getMonth(tokens[i].lower())
                if mon is not "0":
                    if i+1<len(tokens) and tokens[i + 1].isdigit():
                        term=self.dateFormat(mon, tokens[i+1])
                        i=i+1
                    else:
                        term=tokens[i]

                #check if its range pattern: "between Number and Number"
                elif i+3<len(tokens) and tokens[i].lower() == "between" and self.isNumber(tokens[i+1]) and \
                        tokens[i+2].lower() == "and" and self.isNumber(tokens[i+3]):
                    term="between "+tokens[i+1]+" and "+tokens[i+3]
                    terms.extend([tokens[i+1],tokens[i+3]])
                    i=i+3
                #range
                elif '-' in tokens[i]:
                    rangeTokens=tokens[i].split('-')
                    #Word-Word-Word
                    if len(rangeTokens) == 3:
                        terms.extend([rangeTokens[0],rangeTokens[1],rangeTokens[2]])
                        term=tokens[i]
                    else:
                        t1=rangeTokens[0]
                        t2=rangeTokens[1]
                        if self.isNumber(rangeTokens[0]):
                            # Number -
                            j,t1=self.calcSize(rangeTokens,0)
                            if rangeTokens[1] == "percent":
                                term= rangeTokens[0]+"%"

                        if self.isNumber(rangeTokens[1]):
                            # - Number
                            if i+1<len(tokens) and tokens[i+1].lower() in size:
                                j,t2=self.calcSize([rangeTokens[1],tokens[i+1]],0)
                                i=i+1
                            else:
                                j,t2=self.calcSize(rangeTokens[1],0)
                        #add to terms list range right value and range left value
                        terms.extend([t1,t2])
                        if term == "":
                            term=t1+"-"+t2
                else:
                    tokens[i].replace(',','').replace('.','')
                    term=tokens[i]
            terms.append(term)
            i=i+1

        if withStemming is True:
            return self.stem(terms)
        else:
            return terms

    def str_to_number(self,num):
        """
        this function take a string vaule and return the numeric value
        :param num: strin to convert
        :return: numeric value
        """
        return ast.literal_eval("".join(num.split(",")))


    def calcSize(self,tokens, i):
        """
        this methode assest the size of the number
        :param tokens: list of tokens
        :param i:index in the token list
        :return: term insteade of 1,000,000 -> 1M , 1.5 million - > 1.5M 1 trillion -> 1000B
        change the sizes to K/M/B
        and return the last index the function work on
        """
        term = ""
        fraction = " "
        sizes = {"thousand": 1000, "million": 1000000, "billion": 1000000000, "trillion": 1000000000000}
        x = self.str_to_number(tokens[i])
        if i+1 < len(tokens):
            if sizes.__contains__(tokens[i+1].lower()):
                x = x * (sizes[tokens[i+1].lower()])
                i = i + 1
            elif self.isFraction(tokens[i+1]):
                fraction += tokens[i+1]
                i = i + 1
            else:
                fraction=""
        #claasify the size of the number
        if x < sizes["thousand"]:
            term = str(x) + fraction

        elif sizes["thousand"] <= x < sizes["million"]:
            if x % 1000 == 0:
                term = str(int(x/sizes["thousand"]))+"K"
            else:
               term = str(x/sizes["thousand"]) + "K"

        elif sizes["million"] <= x < sizes["billion"]:
            if  x % sizes["million"] == 0:
                term = str(int(x/sizes["million"]))+"M"
            else:
                term = str(x/sizes["million"]) + "M"

        elif x >= sizes["billion"]:
            if x % sizes["billion"] == 0:
                term = str(int(x / sizes["billion"])) + "B"
            else:
                term = str((x / sizes["billion"])) + "B"

        return i, term


    def isFraction(self, fraction):
        """
        check if string is a fraction from the formst X/Y
        :param fraction: string to chech
        :return: True - is a fraction
        """
        list=[]
        if '/' in fraction:
            list = fraction.split("/")
            return list[0].isnumeric() and list[1].isnumeric()
        else:
            return False

    #get num of month and day, return date format MM-DD or YYYY-MM
    def dateFormat(self, month, number):

        if int(number)<10:
            number= "0"+number
        if int(number)>31:
            return number + "-" + month
        else:
            return month + "-" + number

    #param- name of month
    #return the month number or  if its not a month
    def getMonth(self, month):
        i=0
        while i < 12:
            if month == months[2*i+1] or month == months[2*i]:
                if i < 10:
                    return "0"+str(i+1)
                else:
                    return str(i+1)
            i+=1

        return "0"

    #param- token
    #return true if its a number or fraction
    def isNumber(self, token):

        #1st- regular expression that detect number like X,YYY  or X,YYY.ZZ
        return re.match("^(\d+|\d{1,3}(,\d{3})*)(\.\d+)?$",token) or self.isFraction(token)

    # def isFraction(self, token):
    #     # regular expression that can detect fraction from the pattern X/Y
    #     return re.match("([1-9]\/[1-9])", token)

    #return price term according price term rules
    #change to push
    def calcPrice(self, tokens, i, flag):

        term = ""
        fraction = " "
        sizes = {"m": 1000000, "million": 1000000, "billion": 1000000000, "bn": 1000000000, "trillion": 1000000000000}
        orginalToken = tokens[i]
        x = self.str_to_number(tokens[i])
        if i + 1 < len(tokens):
            if tokens[i + 1].lower() in sizes:
                x = x * (sizes[tokens[i + 1].lower()])
                i = i + 1

        # claasify the size of the number
        if x < sizes["million"]:
            if i + 1 < len(tokens) and self.isFraction(tokens[i + 1]):
                fraction += tokens[i + 1]
                i = i + 1
                return i + 1, orginalToken + fraction + " " + "Dollars"
            elif flag:
                term = orginalToken + " Dollars"
            else:
                term = orginalToken + " Dollars"
                if i + 1 < len(tokens) and tokens[i + 1] == 'dollars':
                    i = i + 1


        else:
            if x % sizes["million"] == 0:
                term = str(int(x / sizes["million"])) + "M"
            else:
                term = str(x / sizes["million"]) + "M"

        if flag:
            term += " Dollars"
        elif i + 1 < len(tokens) and tokens[i + 1].lower() == "dollars":
            term += " Dollars"
            i = i + 1
        elif i + 2 < len(tokens) and tokens[i + 1].lower() == "u.s." and tokens[i + 2].lower() == "dollars":
            term += " Dollars"
            i = i + 2
        return i, term

    def stem(self, tokens):
        terms=[]
        ps = PorterStemmer()
        for token in tokens:
            terms.append(ps.stem(token))
        return terms







