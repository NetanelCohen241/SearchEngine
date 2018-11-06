import nltk
import ast
import re

months = ["january", "jan", "february", "feb", "march", "mar", "april", "apr", "may", "may", "june", "jun", "july", "jul",
          "august", "aug", "september", "sep", "october", "oct", "november", "nov", "december", "dec"]

sizes = ["trilion", "bilion", "milion", "thousand"]
class Parser:

    def __init__(self):

        self.terms=[]


    def parse(self,text):
        i=0
        term=""
        terms=[]
        tokens= (str(text).replace(':','').replace('"','').replace('!','').replace('?','').replace('*','')
                 .replace('(','').replace(')','').replace('[','').replace(']','').replace('{','').replace('}','').split(' '))

        while i < len(tokens):

            if tokens[i].isdigit():
                # Date
                mon= self.getMonth(tokens[i+1].lower())
                if mon!=0:
                    term=self.dateFormat(mon, tokens[i])
                    i=i+1
            #Price
            elif tokens[i].startswith("$",0,1):
                tokens[i]=tokens[i].replace('$', '')
                j, term = self.calcPrice(tokens[i].replace('-',' ').split(), 0, True)
            #Percent
            elif tokens[i].endswith("%",len(tokens[i])-1):
                if self.isNumber(tokens[i].replace('%','')):
                    term= tokens[i]+"%"
            # Number
            elif self.isNumber(tokens[i]):

                #Percent
                if i+1<len(tokens) and (tokens[i+1] is "percent" or tokens[i+1] is "percentage"):
                    term=tokens[i+1]+"%"
                    i=i+1
                #Price
                elif (i+1<len(tokens) and tokens[i+1] is "Dollars") or (i+2<len(tokens) and (tokens[i+2] is "Dollars" or tokens[i+2] is "U.S.")):
                    i,term= self.calcPrice(tokens, i, False)
                #Number(only size)
                else:
                    #number range
                    if i+1<len(tokens) and '-' in tokens[i+1]:
                        rangeTokens=tokens[i+1].split('-')
                        if rangeTokens[0].lower() in sizes:
                            #left value in range
                            j,t=self.calcSize([tokens[i],rangeTokens[0]],0)
                            terms.append(t)
                            term=t
                        if self.isNumber(rangeTokens[1]):
                            # Number-Number
                            if i+2<len(tokens) and tokens[i+2].lower() in sizes:
                                j, t2 = self.calcSize([rangeTokens[0], tokens[i+2]], 0)
                                terms.append(t2)
                                term=term+"-"+t2
                        #Number-Word
                        else:
                            term=term+"-"+rangeTokens[1]

                    else:
                        i,term=self.calcSize(tokens,i)

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
                elif i+3<len(tokens) and tokens[i].lower() is "between" and self.isNumber(tokens[i+1]) and \
                        tokens[i+2].lower() is "and" and self.isNumber(tokens[i+3]):
                    term="between "+tokens[i+1]+" and "+tokens[i+3]
                    terms.append({tokens[i+1],tokens[i+3]})
                    i=i+3
                #range
                elif '-' in tokens[i]:
                    rangeTokens=tokens[i].split('-')
                    #Word-Word-Word
                    if len(rangeTokens) is 3:
                        terms.append({rangeTokens[0],rangeTokens[1],rangeTokens[2]})
                        term=tokens[i]
                    else:
                        t1=rangeTokens[0]
                        t2=rangeTokens[1]
                        if self.isNumber(rangeTokens[0]):
                            # Number -
                            j,t1=self.calcSize(rangeTokens,0)
                            if rangeTokens[1] is "percent":
                                term= rangeTokens[0]+"%"

                        if self.isNumber(rangeTokens[1]):
                            # - Number
                            if i+1<len(tokens) and tokens[i+1].lower() in sizes:
                                j,t2=self.calcSize([rangeTokens[1],tokens[i+1]],0)
                            else:
                                j,t2=self.calcSize(rangeTokens[1],0)
                        #add to terms list range right value and range left value
                        terms.append({t1,t2})
                        if term is "":
                            term=t1+"-"+t2
                else:
                    term=tokens[i]
            terms.append(term)
            i=i+1
        return terms

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
            if tokens[i+1].lower in sizes:
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


    def isFraction(self, fraction):
        """
        check if string is a fraction from the formst X/Y
        :param fraction: string to chech
        :return: True - is a fraction
        """
        list = fraction.split("/")
        return list[0].isnumeric() and list[-1].isnumeric()

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
        print(len(months))
        while i < 12:
            if month == months[2*i+1] or month == months[2*i]:
                if i < 10:
                    return "0"+str(i+1)
                else:
                    return ""+str(i+1)
            i+=1

        return ""+str(0)

    #param- token
    #return true if its a number or fraction
    def isNumber(self, token):

        #1st- regular expression that detect number like X,YYY  or X,YYY.ZZ
        return re.match("^(\d+|\d{1,3}(,\d{3})*)(\.\d+)?$",token) or self.isFraction(token)


    #return price term according price term rules
    def calcPrice(self, tokens, i, dolarFlag):

        term=""
        # term= ""+self.calcPriceValue()


        return i,term






