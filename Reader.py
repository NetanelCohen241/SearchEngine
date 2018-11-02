import os
import re


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




