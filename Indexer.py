import os

import Reader
import Parse

class PostingElement(object):
    """
    This class represents an element in the posting list:
    doc number,   term frequency,   term locations, whether the term is part of doc title
    """
    def __init__(self, doc_no, term_details, in_title):
        self.docNo=doc_no
        self.termDetails=term_details
        self.inTitle=in_title

    def to_string(self):
        return self.docNo.replace(" ",'') +"," + str(self.termDetails.to_string()) + "," + str(self.inTitle)


class City(object):
    def __init__(self):
        self.currency=""
        self.population=""
        self.name=""

    def to_string(self):
        return "{0}            {1}            {2}" \
            .format(self.name, self.currency, self.population)


class Index(object):

    def __init__(self,corpus_path,posting_list_path,city_dict, stop_words):
        self.corpusPath=corpus_path
        self.postingListPath=posting_list_path
        self.city_dict_from_api=city_dict
        self.parser = Parse.Parser(stop_words)
        # self.docs=[]

    def create_index(self, with_stemming, pid, block_size):
        """
        This function creates an inverted index.
        :param block_size:
        :param with_stemming: determines whether do stemming or not
        :param pid: number of chunk to read.
        :return: a dictionary: key=term, value= how many the term appeared in the doc(tf)
        """
        posting_list = {}
        city = {}
        language={}
        read=Reader.ReadFile(self.corpusPath)
        doc_list=read.startAction(pid*block_size,block_size)

        for doc in doc_list:
            doc_dictionary,max_tf=self.parser.parse(doc.txt+" "+doc.city+" "+" ".join(doc.title),with_stemming)
            doc.title,z=self.parser.parse(" ".join(doc.title),with_stemming)
            doc.title=doc.title.keys()
            doc.set_num_of_uniqe_terms(len(doc_dictionary.keys()))
            doc.set_maxtf(max_tf)
            length=0
            for doc_num in doc_dictionary:
                length+=doc_dictionary[doc_num]
            doc.length=length
            if not language.__contains__(doc.language) and doc.language != "None":
                language[doc.language]=""
            self.insert_to_posting_list(posting_list, doc_dictionary, doc)
            self.insert_to_city(city,doc)
        self.write_city_to_disk(city, pid)
        self.write_docs_to_disk(doc_list,with_stemming)
        self.write_language_to_disk(language)
        self.write_posting_list_to_disk(posting_list, pid, with_stemming)


    def insert_to_posting_list(self, posting_list, doc_dictionary, doc):
        """
        This function inserts an element into posting list
        :param posting_list: dictionary of all documents- key=term value=doc numbers,tf,locations,whether the term is in doc title
        :param doc_dictionary: element to insert
        :param doc: doc object
        :return:
        """
        for key in doc_dictionary.keys():
            in_title="F"
            term=doc_dictionary[key]
            if key in doc.title:
                in_title="T"
            if posting_list.__contains__(key):
                posting_list[key].append(PostingElement(doc.docNumber, term, in_title))
            else:
                posting_list[key] = []
                posting_list[key].append(PostingElement(doc.docNumber, term, in_title))

    def insert_to_city(self, my_city, doc):
        if doc.city=="" or doc.city==[] or doc.city=="--":
            return
        doc_city,t=self.parser.parse(doc.city.lower(),False)
        if not doc_city:
            return
        doc_city=list(doc_city.keys())[0]
        doc_city=doc_city.lower()
        if doc_city in my_city.keys():
            return
        city_obj = City()
        if doc_city in self.city_dict_from_api:
             data = self.city_dict_from_api[doc_city]
             city_obj.name = data[0]
             city_obj.currency = data[1]
             trash,city_obj.population = self.parser.calcSize([data[2]], 0)
        else:
            city_obj.name = "N"
            city_obj.currency = "N"
            city_obj.population = "0"
        my_city[doc_city.upper()] = city_obj


    def write_posting_list_to_disk(self, posting_list, pid, with_stemming):
        """
        This function sorts the posting list and writes it into the disk.
        :param with_stemming:
        :param posting_list: given posting list
        :param pid:
        :return:
        """
        if with_stemming:
            name="postingWithStemming" + str(pid) + ".txt"
        else:
            name = "posting" + str(pid) + ".txt"
        with open(name, "w+", -1, "utf-8") as out:

            for key in sorted(posting_list.keys(), key=str.lower):
                if key == "":
                    continue
                out.write(key+ ":")
                for element in posting_list[key]:
                    out.write(element.to_string() + " ")
                out.write("\n")
        out.close()


    def write_docs_to_disk(self, doc_list, stem):
        """
        This function writes the given doc list to disk- doc number , num of uniqe terms,
        :param doc_list:
        :return:
        """
        with open(self.postingListPath +"/docsStem.txt" if stem else self.postingListPath +"/docs.txt", "a+") as out:
            for doc in doc_list:
                out.write(doc.to_string() + "\n")
        out.close()

    def write_language_to_disk(self, language):
        with open("language.txt", "a+") as out:
            for key in language:
                    out.write(key + "\n")
        out.close()

    ##write city to disc
    def write_city_to_disk(self, city, pid):
        if not city.keys():
            return
        with open("city" + str(pid) + ".txt", "w+") as out:

            for key in city.keys():
                out.write(key + ":           " + city[key].to_string() + " ")
                out.write("\n")
        out.close()












