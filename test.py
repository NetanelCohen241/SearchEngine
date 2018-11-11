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




def BeautifulTags(txt, tag, returnWithoutTag):
        ans = []
        soup = bs4.BeautifulSoup(txt, 'html.parser')
        tagdata = soup.find_all(tag.lower())
        for iter in tagdata:
            if returnWithoutTag:
                ans.append(iter.get_text())
            else:
                ans.append(str(iter))
        return ans

# d = defaultdict(int)
# with open("FB396001",'r') as f:
#     txt=f.read()
#     for word in nltk.word_tokenize(re.sub('\W+', ' ', txt)):
#         d[word] += 1
#     print(d)


def splitTags(txt):
    ans=[]
    docList = txt.split("</DOC>\n\n<DOC>")
    for i in docList:
        docNumber= re.findall(r'<DOCNO>(.*?)</DOCNO>',i)
        if i.__contains__("<F"):
            docCity=re.findall(r'<F P=104>(.*?)</F>',i)
            if len(docCity) > 0 and docCity[0] != "":
               docCity=docCity[0]
        else:
            docCity = ""
        textContent= (i.split("<TEXT>")[1]).split("</TEXT")[0]
        doc = Doc.Document(docNumber,textContent,docCity)
        ans.append(doc)
    return ans


with open("FB396001","r") as f:
    ftxt=f.read()
    t=time.time()
    split=splitTags(ftxt)
    for i in split:
        print(i.toString())
    print(time.time()-t)
