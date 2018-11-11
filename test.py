from collections import defaultdict

import bs4
import nltk

import Doc
import Parse
import Reader
import re
import time
import  Parse
from bs4 import BeautifulSoup

# d = defaultdict(int)
# with open("FB396001",'r') as f:
#     txt=f.read()
#     for word in nltk.word_tokenize(re.sub('\W+', ' ', txt)):
#         d[word] += 1
#     print(d)

r=Reader.ReadFile("")
with open("FB396001","r") as f:
    ftxt=f.read()
    t=time.time()
    split=r.splitTags(ftxt)
    for i in split:
        print(i.toString())
    print(time.time()-t,len(split))
#
# check=['1.76 dollars','60,000 dollars']
# x=Parse.Parser()
# for c in check:
#     print("orginal value: " + c," ==> ")
#     print(x.calcPrice(c.split(),0,False))