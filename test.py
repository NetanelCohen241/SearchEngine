import nltk
import time
import re
import  Parse
from bs4 import BeautifulSoup

# r = Reader.ReadFile("D:\iretrival\corpus")
import Reader

x = Parse.Parser()

# with open("FB396006", "r") as fin:
#     txt=fin.read()
#     # print(Reader.ReadFile.separeteTags(None,txt,"docno",False))
#     with open("tes","w") as out:
#         out.write("".join(txt.replace("</DOCNO>","<DOCNO>").split("<DOCNO>")))
#         out.close()
#     print(txt.split("<DOCNO>"))
#below 1 million
underM =[
"1,890 Dollars",
"450 56/90 Dollars",
"$559,000"]

upM= [
"1.55 million U.S. dollars",
"0.7 trillion U.S. dollars"
]

Ranges= [
"23,000,000-toys",
"$239-Million",
"100 million-toys",
"cash-45 million",
"23,000,000 Dollars",
"$23,987,000",
"$1.89 million",
"$55 billion",
"$1.8 trillion",
"9 m Dollars",
"1.76 bn Dollars",
"6 billion U.S. dollars",
"1.55 million U.S. dollars",
"0.7 trillion U.S. dollars",
"55 billion-100 thousand",
"whats-up-baby"
]
Range= [
"55 billion-100 thousand",
]



print("Ranges\n")
terms=""
for t in upM:
    terms=terms+" "+t

print(x.parse(terms+" it is a students studied words",True))


# y=nltk.word_tokenize("1,000,400")
# print(y)
# z= ["12.34", "1.4","100","1,000","1000","76,023,000,000" , "13,000,000","10,764","1010.98","75.4 thousand","55 thousand","55 million","34 billion",
    # "1.5 trillion","7 Trillion","0.4 billion","0.24 trillion","1.5 billion","130 3/5", "1 32/99","1000500","98000000123"]
# with open("FB396001","r") as fin:
    # x=fin.read()
# t= time.time()
# # x.replace(",", " ").replace("%"," ").replace("("," ").replace(")"," ").replace(":"," ").replace("\""," ").split()
# re.split("[, \-!()$%#@&?:]+", x)
# print(time.time()-t)
# w=[]
# for t in z:
#     yy=nltk.word_tokenize(t)
#     i, term = x.calcSize(yy, 0)
#     w.append(term)
# df = pandas.DataFrame({"original value ":z,"calcsize value":w})
# print(df)
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