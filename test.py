import nltk
import time
import re
import  Parse
from bs4 import BeautifulSoup

# r = Reader.ReadFile("D:\iretrival\corpus")
import Reader

x = Parse.Parser()

with open("FB396002", "r") as fin:
    txt=fin.read()
    print(Reader.ReadFile.separeteTags(None,txt,"docno",False))

#below 1 million
# underM =[
# "$400"
# "1,890 Dollars",
# "450 56/90 Dollars",
# "$559,000"]
#
# upM= [
# "23,000,000 Dollars",
# "$23,987,000",
# "$1.89 million",
# "$55 billion",
# "$1.8 trillion",
# "9 m Dollars",
# "1.76 bn Dollars",
# "6 billion U.S. dollars",
# "1.55 million U.S. dollars",
# "0.7 trillion U.S. dollars"
# ]
# print(x.calcPrice([':10,000'],0))