from collections import defaultdict

import nltk

import Doc
import Parse
import Reader
import re
import time
import  Parse
# d = defaultdict(int)
# with open("FB396001",'r') as f:
#     txt=f.read()
#     for word in nltk.word_tokenize(re.sub('\W+', ' ', txt)):
#         d[word] += 1
#     print(d)

# r=Reader.ReadFile("")
# with open("FB396001","r") as f:
#     ftxt=f.read()
#     t=time.time()
#     split=r.splitTags(ftxt)
#     for i in split:
#         print(i.toString())
#     print(time.time()-t,len(split))
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
"$559,000"
]

upM= [
"$23,987,000",
"$1.89 million",
"$55 billion",
"$1.8 trillion",
"9 m Dollars",
"1.55 million U.S. dollars",
"0.7 trillion U.S. dollars"
]

Ranges= [
# "23,000,000-toys",
# "$239-Million",
"100 million-toys",
"cash-45 million",
"23,000,000 Dollars",
"$23,987,000",
    "1000.344",
    "240 8/9",
"$1.89 million",
"$55 billion",
"$1.8 trillion",
"9 m Dollars",
"1.76 bn Dollars",
"6 billion U.S. dollars",
"1.55 million U.S. dollars",
"0.7 trillion U.S. dollars",
"55 billion-100 thousand",
"whats-up-baby",
"14 May 14 january June 1992 1.766 Dollars 5 3/4 Dollars 60,000 Dollars 5 bn Dollars 17 7/99 imNot-your/toy 222% 8787878 percent 800 Billion check 10,230,555,000,000 1010.56333 between 55,000 and 450,000 "
]
Range= [
"55 billion-100 thousand",
]


x=Parse.Parser()
print("Ranges\n")
terms=""
for t in Ranges:
    terms=terms+" "+t

# print(x.parse("22/13 33/55",False))
# print(x.calcSize(["33/55"],0))

#
r=Reader.ReadFile("C:\\Users\Daniel\Desktop\לימודים\שנה ג\אחזור מידע\פרויקט מנוע חלק א\corpus\corpus")
t=time.time()
list=r.startAction(500)
ans=[]
i=0
for doc in list:
    ans.extend(x.parse("065",False))
    # print(i)
    i+=1
print(time.time()-t)