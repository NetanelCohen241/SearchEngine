import os
import re
import bs4

import Doc


class ReadFile(object):

    def __init__(self, path):
        self.path = path
        if not os.path.isdir("documents"):
            os.mkdir("documents")

    def startAction(self):
        self.scanDir(os.listdir(self.path))

    def scanDir(self, dirList):
        for dirName in dirList:
            with open(self.path + "/" + dirName + "/" + dirName,"r") as fin:
                y= fin.read()
                docList=re.findall(r"<DOC.*?>(.*?)</DOC>",y,re.DOTALL)
                docNames=re.findall(r"<DOCNO.*?>(.*?)</DOCNO>",y,re.DOTALL)
                self.makeFiles(docList,docNames)

    def makeFiles(self, docsContent, docNames):

        for i in range(len(docNames)):
            file = open("documents/"+docNames[i],"w")
            file.write(docsContent[i])
            file.close()

    def separeteTags(self,txt, tag, returnWithoutTag):
        """
        this method separete txt throw its givaen tag for exsample:
        <TEXT>
            this is text
        </TEXT>
        <TEXT>
            another text
        </TEXT>
        the function return a string list of ['this is text', 'another text']
        :param txt: text you want to separate
        :param tag: tha tag you eant i'ts data
        :param returnWithoutTag: TRUE - return ['<text>this is text</text>', '<text>another text</text>']
        :return: list of string
        """
        ans = []
        soup = bs4.BeautifulSoup(txt, 'html.parser')
        tagdata = soup.find_all(tag.lower())
        for iter in tagdata:
            if returnWithoutTag:
                ans.append(iter.get_text())
            else:
                ans.append(str(iter))
        return ans

    def splitTags(self,txt):
        """
        this function get text of file and return list of all document inside as an object that incude id number
        city,and text content ( string between <text< tag>
        :param txt: string of a file that conatain <doc> tag
        :return:  list of document object
        """
        ans = []
        docList = txt.split("</DOC>\n\n<DOC>")
        for i in docList:
            docNumber = re.findall(r'<DOCNO>(.*?)</DOCNO>', i)[0]
            if i.__contains__("<F"):
                docCity = re.findall(r'<F P=104>(.*?)</F>', i)
                if len(docCity) > 0 and docCity[0] != "":
                    docCity = docCity[0].split()[0].upper()
            else:
                docCity = ""
            textContent = (i.split("<TEXT>")[1]).split("</TEXT")[0]
            doc = Doc.Document(docNumber, textContent, docCity)
            ans.append(doc)
        return ans
