import ast
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

    def str_to_number(self,num):
        """
        this function take a string vaule and return the numeric value
        :param num: strin to convert
        :return: numeric value
        """
        return ast.literal_eval("".join(num.split(",")))


    #TODO:Twitoo
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
        list = fraction.split("/")
        return list[0].isnumeric() and list[-1].isnumeric()

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

    # def isFraction(self, token):
    #     # regular expression that can detect fraction from the pattern X/Y
    #     return re.match("([1-9]\/[1-9])", token)

    #return price term according price term rules
    def calcPrice(self, tokens, i, flag):

        term = ""
        fraction = " "
        sizes = {"m": 1000000, "million": 1000000, "billion": 1000000000,"bn":1000000000, "trillion": 1000000000000}
        orginalToken=tokens[i]
        x = self.str_to_number(tokens[i])
        if i + 1 < len(tokens):
            if tokens[i + 1].lower() in sizes:
                x = x * (sizes[tokens[i + 1].lower()])
                i = i + 1

        # claasify the size of the number
        if x < sizes["million"]:
            if i+1 < len(tokens) and self.isFraction(tokens[i + 1]):
                fraction += tokens[i + 1]
                i=i+1
                return i,orginalToken+fraction+" "+"Dollars"
            elif flag:
                term = orginalToken + " Dollars"
            else:
                term = orginalToken + " Dollars"


        else:
            if x % sizes["million"] == 0:
                term = str(int(x/sizes["million"])) + "M"
                if flag:
                    term += " Dollars"
                    i = i + 1
                elif i+1 < len(tokens) and tokens[i+1].lower() == "dollars":
                    term += " Dollars"
                    i = i + 1
                elif i+2 < len(tokens) and tokens[i+1].lower() == "u.s." and tokens[i+2].lower() == "dollars":
                    term += " Dollars"
                    i = i+1
            else:
                term = str(x / sizes["million"]) + "M Dollars"
        return i, term






