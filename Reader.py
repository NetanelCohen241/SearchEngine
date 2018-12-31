import os
import re
import Doc


class ReadFile(object):

    def __init__(self, path):
        self.path = path
        if not os.path.isdir("documents"):
            os.mkdir("documents")

    def startAction(self,start,howManyFiles):
        return self.scanDir(os.listdir(self.path),start,howManyFiles)

    def scanDir(self, dirList, start, howManyFiles):
        """
        This function
        :param dirList: list of all directories
        :param start: from which
        :param howManyFiles:
        :return:
        """
        ans=[]
        for i in range(start,start+howManyFiles):
            with open(self.path + "/" + dirList[i] + "/" + dirList[i],"r") as fin:
                txt= fin.read()
                ans.extend(self.splitTags(txt))
            fin.close()
        return ans

    def makeFiles(self, docsContent, docNames):

        for i in range(len(docNames)):
            file = open("documents/"+docNames[i],"w")
            file.write(docsContent[i])
            file.close()


    def splitTags(self,txt):
        """
        this function get text of file and return list of all document inside as an object that incude id number
        city,and text content ( string between <text< tag>
        :param txt: string of a file that conatain <doc> tag
        :return:  list of document object
        """
        ans = []
        docList = txt.split("</DOC>")
        docCity=""
        doc_language="None"
        for i in docList:
            if i=="\n" or i=="\n\n" or i=="\n\n\n" or i=="\n\n\n\n" or i=="":
                break
            try:
                docNumber = re.findall(r'<DOCNO>(.*?)</DOCNO>', i)[0].replace(" ","")
                if i.__contains__("<F"):
                    docCity = re.findall(r'<F P=104>(.*?)</F>', i)
                    if len(docCity) > 0 and docCity[0] != "":
                        docCity = docCity[0].split()[0].upper()
                    else:
                        docCity = ""
                textContent=""
                if i.__contains__("<TEXT>"):
                    textContent = (i.split("<TEXT>")[1]).split("</TEXT>")[0]
                    if textContent.__contains__("<F P=105>"):
                        doc_language = re.findall(r'<F P=105>(.*?)</F>', textContent)[0]
                doc = Doc.Document(docNumber,textContent, docCity)
                # if doc.city != "" and docCity!=[]:
                #     self.find_all_locations_in_text(doc)
                if i.__contains__("<DATE1>"):
                    date=re.findall(r'<DATE1>(.*?)</DATE1>', i)[0]
                    doc.set_date(date)
                if i.__contains__("<TI>"):
                    title = (i.split("<TI>")[1]).split("</TI>")[0].split()
                    doc.set_title(title)
                doc.set_language(doc_language)
                ans.append(doc)
            except:
                print("error")
        return ans
