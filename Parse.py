import ast
import re
# import stemmer
from nltk.stem import PorterStemmer

months = ["january", "jan", "february", "feb", "march", "mar", "april", "apr", "may", "may", "june", "jun", "july",
          "jul","august", "aug", "september", "sep", "october", "oct", "november", "nov", "december", "dec"]

size = ["trillion", "billion", "million", "thousand"]

class Term:
    def __init__(self):
        self.frq=0
        self.locations=[]
        # self.last_loc=0


    def to_string(self):
        return "{0},{1}".format(self.frq,self.locations)


class Parser(object):

    def __init__(self, stop_words_path):

        self.trm = []
        self.text=""
        self.stop_words_path=stop_words_path
        self.max_tf=0

    def parse(self, text, with_stemming):

        self.max_tf=0
        doc_dictionary = {}
        if text=="":
            return doc_dictionary
        self.text = self.clean_txt(text)
        doc_dictionary = self.parseRules(doc_dictionary)

        if with_stemming is True:
            doc_dictionary = self.stem(doc_dictionary)
        return doc_dictionary

    def str_to_number(self, num):
        """
        this function take a string vaule and return the numeric value
        :param num: strin to convert
        :return: numeric value
        """
        return ast.literal_eval("".join(num.split(",")))

    def calcSize(self, tokens, i):
        """
        this methode assest the size of the number
        :param tokens: list of tokens
        :param i:index in the token list
        :return: term insteade of 1,000,000 -> 1M , 1.5 million - > 1.5M 1 trillion -> 1000B
        change the sizes to K/M/B
        and return the last index the function work on
        """
        # print(tokens[i])
        term = ""
        fraction = ""
        if self.isFraction(tokens[i]):
            return i, tokens[i]
        if tokens[i].startswith('0') and tokens[i].isdigit():
            return i, tokens[i]
        sizes = {"thousand": 1000, "million": 1000000, "billion": 1000000000, "trillion": 1000000000000}
        x = self.str_to_number(tokens[i])
        if i + 1 < len(tokens):
            if sizes.__contains__(tokens[i + 1].lower()):
                x = x * (sizes[tokens[i + 1].lower()])
                i = i + 1
            elif self.isFraction(tokens[i + 1]):
                fraction += tokens[i + 1]
                i = i + 1
        # claasify the size of the number
        if x < sizes["thousand"]:
            if fraction != "":
                term = str(x) + " " + fraction
            else:
                term = str(x)

        elif sizes["thousand"] <= x < sizes["million"]:
            if x % 1000 == 0:
                term = str(int(x / sizes["thousand"])) + "K"
            else:
                term = "{0:.3f}".format(x / sizes["thousand"]) + "K"

        elif sizes["million"] <= x < sizes["billion"]:
            if x % sizes["million"] == 0:
                term = str(int(x / sizes["million"])) + "M"
            else:
                term = "{0:.3f}".format(x / sizes["million"]) + "M"

        elif x >= sizes["billion"]:
            if x % sizes["billion"] == 0:
                term = str(int(x / sizes["billion"])) + "B"
            else:
                term = "{0:.3f}".format((x / sizes["billion"])) + "B"

        return i, term

    def isFraction(self, fraction):
        """
        check if string is a fraction from the formst X/Y
        :param fraction: string to chech
        :return: True - is a fraction
        """
        list = fraction.split("/")
        if len(list) == 1:
            return False
        return list[0].isnumeric() and list[-1].isnumeric()

    # get num of month and day, return date format MM-DD or YYYY-MM
    def dateFormat(self, month, number):

        if int(number) < 10:
            number = "0" + number
        if int(number) > 31:
            return number + "-" + month
        else:
            return month + "-" + number

    # param- name of month
    # return the month number or  if its not a month
    def getMonth(self, month):
        i = 0
        while i < 12:
            if month == months[2 * i + 1] or month == months[2 * i]:
                if i < 10:
                    return "0" + str(i + 1)
                else:
                    return str(i + 1)
            i += 1

        return "0"

    # param- token
    # return true if its a number or fraction
    def isNumber(self, token):

        # 1st- regular expression that detect number like X,YYY  or X,YYY.ZZ
        return re.match("^(\d+|\d{1,3}(,\d{3})*)(\.\d+)?$", token) or self.isFraction(token)

    # def isFraction(self, token):
    #     # regular expression that can detect fraction from the pattern X/Y
    #     return re.match("([1-9]\/[1-9])", token)

    # return price term according price term rules
    # change to push
    def calcPrice(self, tokens, i, flag):

        term = ""
        fraction = " "
        alreadyAdd = False
        if tokens[i].startswith('0') and tokens[i].isdigit():
            return i, tokens[i]

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
                return i, orginalToken + fraction + " " + "Dollars"
            elif flag:
                term = orginalToken + " Dollars"
                alreadyAdd = True
            else:
                term = orginalToken + " Dollars"
                if i + 1 < len(tokens) and tokens[i + 1].lower() == 'dollars':
                    i = i + 1


        else:
            if x % sizes["million"] == 0:
                term = str(int(x / sizes["million"])) + "M"
                # i=i+1
            else:
                term = "{0:.3f}".format(x / sizes["million"]) + "M"
        # i=i+1
        if flag and not alreadyAdd:
            term += " Dollars"
        elif i + 1 < len(tokens) and tokens[i + 1].lower() == "dollars":
            term += " Dollars"
            i = i + 1
        elif i + 2 < len(tokens) and tokens[i + 1].lower() == "u.s." and tokens[i + 2].lower() == "dollars":
            term += " Dollars"
            i = i + 2
        return i, term

    def stem(self, docDictionary):

        tempDict = {}
        ps = PorterStemmer()
        for key in docDictionary.keys():
            term = ps.stem(key)
            if tempDict.__contains__(term):
                tempDict[term] += docDictionary[key]
            else:
                tempDict[term] = docDictionary[key]

        return tempDict

    def parseRules(self, docDictionary):

        i = 0

        tokens = self.text.replace("--","").replace("/F","").split(' ')
        stop_words={}
        with open(self.stop_words_path+"/stop_words.txt", "r") as sw:
            lines= sw.readlines()
            for line in lines:
                stop_words[line[:len(line)-1]]=""
            sw.close()
            while i < len(tokens):
                term=""
                try:
                    if tokens[i].lower() in stop_words or tokens[i] in ['-', "--", ',', '.', ''] or tokens[i] == "/F":
                        i = i + 1
                        continue
                    if tokens[i] == "0":
                        term = tokens[i]

                    if tokens[i].endswith(',') or tokens[i].endswith('.'):
                        tokens[i] = tokens[i].replace(',', '').replace('.', '')
                        term = tokens[i]
                    # Price
                    if tokens[i].startswith("$", 0, 1) and self.isNumber(tokens[i][1:]):
                        tokens[i] = tokens[i].replace('$', '')
                        if '-' in tokens[i]:
                            j, term = self.calcPrice(tokens[i].replace('-', ' ').split(' '), 0, True)
                        elif i + 1 < len(tokens):
                            j, term = self.calcPrice([tokens[i], tokens[i + 1]], 0, True)
                            i += j
                        else:
                            j, term = self.calcPrice([tokens[i]], 0, True)


                    # Percent
                    elif tokens[i].endswith("%", len(tokens[i]) - 1):
                        tokens[i] = tokens[i].replace('%', '')
                        if self.isNumber(tokens[i]):
                            i, term = self.calcSize(tokens, i)
                            term += "%"
                        else:
                            term = tokens[i]
                    elif self.isFraction(tokens[i]):
                        term = tokens[i]
                    # Number
                    elif self.isNumber(tokens[i]):

                        # Percent
                        if i + 1 < len(tokens) and (
                                tokens[i + 1].lower().replace(',', '').replace('.', '') == "percent" or
                                tokens[i + 1].lower().replace(',', '').replace('.', '') == "percentage"):
                            i, term = self.calcSize(tokens, i)
                            term += '%'
                            i = i + 1
                        # Price
                        elif (i + 1 < len(tokens) and tokens[i + 1].lower().replace(',', '').replace('.',
                                                                                                     '') == "dollars") or \
                                (i + 2 < len(tokens) and (
                                        tokens[i + 2].lower().replace(',', '').replace('.', '') == "dollars" or tokens[
                                    i + 2] == "U.S.")):
                            i, term = self.calcPrice(tokens, i, False)
                        # Number(only size)
                        else:
                            acc = 0
                            # number range
                            if i + 1 < len(tokens) and '-' in tokens[i + 1]:
                                rangeTokens = tokens[i + 1].split('-')
                                if rangeTokens[0].lower() in size:
                                    # left value in range
                                    j, t = self.calcSize([tokens[i], rangeTokens[0]], 0)
                                    self.addToDictionary(docDictionary,[t],i)
                                    term = t
                                    acc = acc + 1
                                    if self.isNumber(rangeTokens[1]):
                                        # Number-Number
                                        if i + 2 < len(tokens) and tokens[i + 2].lower() in size:
                                            j, t2 = self.calcSize([rangeTokens[1], tokens[i + 2]], 0)
                                            self.addToDictionary(docDictionary, [t2],i)
                                            term = term + "-" + t2
                                            i = i + acc + 1
                                        else:
                                            term = tokens[i + 1]
                                    # Number-Word
                                    else:
                                        i = i + 1
                                        term = term + "-" + rangeTokens[1]
                                else:
                                    term = tokens[i]
                            elif tokens[i].isdigit():
                                # Date
                                if i + 1 < len(tokens):
                                    mon = self.getMonth(tokens[i + 1].lower())
                                    if mon is not "0":
                                        term = self.dateFormat(mon, tokens[i])
                                        i = i + 1
                                    elif tokens[i + 1].replace(",", '') == "GMT":
                                        term = tokens[i + 1][:2] + "_" + tokens[i + 1][2:]
                                        i = i + 1
                                    else:
                                        i, term = self.calcSize(tokens, i)
                                else:
                                    i, term = self.calcSize(tokens, i)
                            else:
                                i, term = self.calcSize(tokens, i)

                    # Word
                    else:
                        # Date
                        mon = self.getMonth(tokens[i].lower())
                        if mon is not "0":
                            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                                term = self.dateFormat(mon, tokens[i + 1])
                                i = i + 1
                            else:
                                term = tokens[i]

                        # check if its range pattern: "between Number and Number"
                        elif i + 3 < len(tokens) and tokens[i].lower() == "between" and self.isNumber(tokens[i + 1]) and \
                                tokens[i + 2].lower() == "and" and self.isNumber(tokens[i + 3]):
                            term = "between " + tokens[i + 1] + " and " + tokens[i + 3]
                            self.addToDictionary(docDictionary, [tokens[i + 1], tokens[i + 3]],i)
                            i = i + 3
                        # range
                        elif '-' in tokens[i]:
                            rangeTokens = tokens[i].split('-')
                            # Word-Word-Word
                            if len(rangeTokens) == 3:
                                self.addToDictionary(docDictionary, [rangeTokens[0], rangeTokens[1], rangeTokens[2]],i)
                                term = tokens[i]
                            else:
                                t1 = rangeTokens[0]
                                t2 = rangeTokens[1]
                                if self.isNumber(rangeTokens[0]):
                                    # Number -
                                    if tokens[i+1]=="GMT":
                                        t1 = rangeTokens[0][:2] + "_" + rangeTokens[0][2:]
                                    else:
                                        j, t1 = self.calcSize(rangeTokens, 0)
                                    if rangeTokens[1] == "percent":
                                        term = rangeTokens[0] + "%"

                                if self.isNumber(rangeTokens[1]):
                                    # - Number
                                    if tokens[i+1]=="GMT":
                                        t2 = rangeTokens[1][:2] + "_" + rangeTokens[1][2:]
                                        if i + 1 < len(tokens) and tokens[i + 1].replace(",", '') == "GMT":
                                            i = i + 1
                                    elif i + 1 < len(tokens) and tokens[i + 1].lower() in size:
                                        j, t2 = self.calcSize([rangeTokens[1], tokens[i + 1]], 0)
                                        i = i + 1
                                    else:
                                        j, t2 = self.calcSize([rangeTokens[1]], 0)
                                # add to terms list range right value and range left value
                                self.addToDictionary(docDictionary,[t1, t2],i)
                                if term == "":
                                    term = t1 + "-" + t2
                        else:
                            term = tokens[i].replace('_','').replace(',', '').replace('.', '').replace('/', ' ').replace('-','')

                except:
                    # print(tokens[i])
                    term = tokens[i]
                try:

                    self.addToDictionary(docDictionary, [term],i)
                except:
                    y=5
                i = i + 1

            return docDictionary,self.max_tf


    def addToDictionary(self, docDictionary, terms, location):


        for i in range(len(terms)):
            term_data=Term()
            if docDictionary.__contains__(terms[i]):
                docDictionary[terms[i]].frq += 1

            else:
                docDictionary[terms[i]] = term_data
                docDictionary[terms[i]].frq=1
            if self.max_tf<docDictionary[terms[i]].frq:
                self.max_tf=docDictionary[terms[i]].frq
            docDictionary[terms[i]].locations.append(location)
            location+=1
            # docDictionary[terms[i]].last_loc = docDictionary[terms[i]].locations[-1]




    def find_all_locations(self,term,start):
        text = self.text.lower()
        locations=[]
        l_start = start
        while True:
            l_start = text.find(term.lower(), l_start)
            if l_start == -1:
                break
            locations.append(l_start)
            l_start += len(term)
        if len(locations) != 0:
            return locations
        return []


    def clean_txt(self, text):
        to_replace = {':': '', '#': '', '&': '', '"': '', '!': '', '?': '', '*': '', '(': '', ')': '',
                      '[': '', ']': '', '{': '', '}': '', '\n': '', '|': '', '\'': '', '^': '', '@': '',
                      '`': '', '+': '', '<': '', '>': '', ';': '', '=': '' }

        size=len(text)
        ans=""
        for i in text:
            if i not in to_replace:
                ans += i
        return ans