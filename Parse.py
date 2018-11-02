from _ctypes import byref
from ctypes import c_int

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
        i=c_int()
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


    #TODO:Twitoo
    def calcSize(self,tokens,i):
        term=""
        return i,term




    def dateFormat(self, month, number):
        pass




