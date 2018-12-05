import ast
import re
from nltk.stem.snowball import EnglishStemmer

months = ["january", "jan", "february", "feb", "march", "mar", "april", "apr", "may", "may", "june", "jun", "july",
          "jul", "august", "aug", "september", "sep", "october", "oct", "november", "nov", "december", "dec"]

size = ["trillion", "billion", "million", "thousand"]


class Term:
    def __init__(self):
        # self.frq=0
        self.locations = []

    def to_string(self):
        ans = "[" + str(self.locations[0])
        for i in range(1, len(self.locations)):
            ans += "," + str(self.locations[i])
        return ans + "]"


class Parser(object):
    def __init__(self, stop_words):

        self.stop_words = stop_words
        self.stem_dict = {}
        self.text = ""
        self.max_tf = 0
        self.location = 0

    def parse(self, text, with_stemming):
        """
        This function manage the parsing process.
        :param text: text to parse
        :param with_stemming: whether to do stemming or not
        :return: pair: <docdictionary, max
        """
        self.location = 0
        self.max_tf = 0
        doc_dictionary = {}
        if text == "":
            return doc_dictionary, self.max_tf
        self.text = self.clean_txt(text)
        doc_dictionary = self.parse_rules(doc_dictionary)

        if with_stemming:
            doc_dictionary = self.stem(doc_dictionary)
        return doc_dictionary, self.max_tf

    def str_to_number(self, num):
        """
        this function take a string vaule and return the numeric value
        :param num: strin to convert
        :return: numeric value
        """
        return ast.literal_eval("".join(num.split(",")))

    def clear_zeros(self, num):
        i = 0
        size = len(num)
        for idx in range(0, size):
            if num[idx] == '0' and idx + 1 < size and num[idx + 1] != ".":
                i = i + 1
            else:
                break
        if i == size:
            return "0"
        return num[i:]

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
        tokens[i] = self.clear_zeros(tokens[i])
        term = ""
        fraction = ""
        if self.isFraction(tokens[i]):
            return i, tokens[i]
        # if tokens[i].startswith('0') and tokens[i].isdigit():
        #     return i, tokens[i]
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
                term = "{0:.2f}".format(x / sizes["thousand"]) + "K"

        elif sizes["million"] <= x < sizes["billion"]:
            if x % sizes["million"] == 0:
                term = str(int(x / sizes["million"])) + "M"
            else:
                term = "{0:.2f}".format(x / sizes["million"]) + "M"

        elif x >= sizes["billion"]:
            if x % sizes["billion"] == 0:
                term = str(int(x / sizes["billion"])) + "B"
            else:
                term = "{0:.2f}".format((x / sizes["billion"])) + "B"

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

    # return price term according price term rules
    # change to push
    def calcPrice(self, tokens, i, flag):
        tokens[i] = self.clear_zeros(tokens[i])
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
                term = "{0:.2f}".format(x / sizes["million"]) + "M"
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

    def stem(self, doc_dictionary):

        temp_dict = {}
        e = EnglishStemmer()
        for key in doc_dictionary.keys():
            if not self.__hasNumbers(key):
                term = e.stem(key)
            else:
                term = key
            if temp_dict.__contains__(term):
                temp_dict[term].locations.extend(doc_dictionary[key].locations)
            else:
                t = Term()
                t.locations = doc_dictionary[key].locations
                temp_dict[term] = t

        return temp_dict

    def __hasNumbers(self, input_string):
        """
        This function check whether to given string contains numbers
        :param input_string:
        :return: bool
        """
        for char in input_string:
            if char.isdigit():
                return True
        return False

    def parse_rules(self, doc_dictionary):

        """
        This function responsible for parsing the text.
        It split the text into tokens. itreate over the tokens and activate the parsing rules on each token
        :param doc_dictionary:
        :return: Dictionary : Key= term , Value= term frequency in the text
        """
        i = 0

        tokens = self.text.replace("--", "").replace("/F", "").split(' ')

        while i < len(tokens):
            term = ""
            try:
                if tokens[i].lower() in self.stop_words or tokens[i] in ['-', "--", ',', '.', ''] or tokens[i] == "/F":
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
                                            tokens[i + 2].lower().replace(',', '').replace('.', '') == "dollars" or
                                            tokens[
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
                                self.add_to_dictionary(doc_dictionary, [t], i)
                                term = t
                                acc = acc + 1
                                if self.isNumber(rangeTokens[1]):
                                    # Number-Number
                                    if i + 2 < len(tokens) and tokens[i + 2].lower() in size:
                                        j, t2 = self.calcSize([rangeTokens[1], tokens[i + 2]], 0)
                                        self.add_to_dictionary(doc_dictionary, [t2], i)
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
                        self.add_to_dictionary(doc_dictionary, [tokens[i + 1], tokens[i + 3]], i)
                        i = i + 3
                    # range
                    elif '-' in tokens[i]:
                        rangeTokens = tokens[i].split('-')
                        # Word-Word-Word
                        if len(rangeTokens) == 3:
                            self.add_to_dictionary(doc_dictionary, [rangeTokens[0], rangeTokens[1], rangeTokens[2]], i)
                            term = tokens[i]
                        else:
                            t1 = rangeTokens[0]
                            t2 = rangeTokens[1]
                            if self.isNumber(rangeTokens[0]):
                                # Number -
                                if tokens[i + 1] == "GMT":
                                    t1 = rangeTokens[0][:2] + "_" + rangeTokens[0][2:]
                                else:
                                    j, t1 = self.calcSize(rangeTokens, 0)
                                if rangeTokens[1] == "percent":
                                    term = rangeTokens[0] + "%"
                            if self.isNumber(rangeTokens[1]):
                                # - Number
                                if tokens[i + 1] == "GMT":
                                    t2 = rangeTokens[1][:2] + "_" + rangeTokens[1][2:]
                                    if i + 1 < len(tokens) and tokens[i + 1].replace(",", '') == "GMT":
                                        i = i + 1
                                elif i + 1 < len(tokens) and tokens[i + 1].lower() in size:
                                    j, t2 = self.calcSize([rangeTokens[1], tokens[i + 1]], 0)
                                    i = i + 1
                                else:
                                    j, t2 = self.calcSize([rangeTokens[1]], 0)
                            # add to terms list range right value and range left value
                            self.add_to_dictionary(doc_dictionary, [t1, t2], i)
                            if term == "":
                                term = t1 + "-" + t2
                    else:
                        term = tokens[i].replace('_', ' ').replace(',', ' ').replace('.', ' ').replace('/',
                                                                                                       ' ').replace('-',
                                                                                                                    ' ').split()
                        self.add_to_dictionary(doc_dictionary, term, i)
                        i += 1
                        continue

            except:
                # print(tokens[i])
                term = tokens[i]
            try:
                self.add_to_dictionary(doc_dictionary, [term], i)
            except:
                y = 5
            i = i + 1
        return doc_dictionary

    def add_to_dictionary(self, doc_dictionary, terms, location):
        """
        This function adds a term into the dictionary.
        If the term is already exist in the dictionary, the function append term location to its value in the dictionary
        :param doc_dictionary: the dictionary to append
        :param terms: list of few terms to append. most of the times it will be one term
        :param location:
        :return:
        """

        for i in range(len(terms)):
            term_data = Term()
            if doc_dictionary.__contains__(terms[i]):
                doc_dictionary[terms[i]].frq += 1

            else:
                doc_dictionary[terms[i]] = term_data
                doc_dictionary[terms[i]].frq = 1
            if self.max_tf < doc_dictionary[terms[i]].frq:
                self.max_tf = doc_dictionary[terms[i]].frq
            doc_dictionary[terms[i]].locations.append(self.location)
            self.location += 1

    def clean_txt(self, text):
        """
        This function cleans(replace with space) special characters from the given text
        :param text:
        :return: the clean text.
        """
        to_replace = {':': '', '#': '', '&': '', '"': '', '!': '', '?': '', '*': '', '(': '', ')': '',
                      '[': '', ']': '', '{': '', '}': '', '\n': '', '|': '', '\'': '', '^': '', '@': '',
                      '`': '', '+': '', '<': '', '>': '', ';': '', '=': ''}

        ans = ""
        for i in text:
            if i not in to_replace:
                ans += i
            else:
                ans += " "
        return ans
