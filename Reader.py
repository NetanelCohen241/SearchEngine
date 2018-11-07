import os
import re
import bs4
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

