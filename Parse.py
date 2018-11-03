import ast
import re
from _ctypes import byref
from ctypes import c_int

import math
import nltk
from enum import Enum


class Month(Enum):
    January = 1
    February = 2
    March = 3
    April = 4




class Parser:

    def __init__(self):

        self.terms=[]


    def parse(self,text):
        i=0
        month = ["january", "jan", "february", "feb", "march", "mar", "april", "apr", "may", "june", "jun", "july", "jul", "august", "aug", "september", "sep", "october", "oct", "november", "nov", "december", "dec"]
        terms=[]
        tokens=nltk.word_tokenize(text)
        while i < len(tokens):

            if tokens[i].isdigit():
                if tokens[i+1].lower() in month:
                    terms.append(self.dateFormat(tokens[i], tokens[i + 1]))
                    i = i + 1
                else:
                    ind,term=self.calcSize(tokens,i)
                    terms.append(term)
                    i=ind
            elif tokens[i] == '$':
                print(5) #TODO
            elif tokens[i].lower() in month:
                if tokens[i + 1].lower() in month:
                    if tokens[i + 1].isdigit():
                        terms.append(self.dateFormat(tokens[i], tokens[i+1]))
                        i=i+1

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

    def dateFormat(self, month, number):
        pass




