import Parse
from Rank import Ranker


class Searcher:

    def __init__(self, queries, dictionary, documents, avgl, posting_path,parser):
        self.queries = queries
        self.ranker = Ranker()
        self.dictionary = dictionary
        self.documents = documents
        self.avgl = avgl
        self.posting_path = posting_path
        self.parser=parser

    def run(self):
        results = dict()
        for query_num in self.queries.keys():
            results[query_num]=self.run_query(self.queries[query_num])

        # need to return the top 50 documents
        return results

    def run_query(self, query):
        query_result = dict()
        query_terms, _ = self.parser.parse(query, False)
        for term in query_terms:
            doc_dict = dict()
            if term.lower() in self.dictionary or term.upper() in self.dictionary:
                self.read_term_postinglist(doc_dict,term)  # retrieve index entry
                for docid in doc_dict:  # for each document and its word frequency
                    score = self.ranker.score_BM25(n=len(doc_dict), f=doc_dict[docid][0], N=len(self.documents),
                                                   dl=self.documents[docid][0],
                                                   avgl=self.avgl, cf=query_terms[term].frq,title=doc_dict[docid][1])  # calculate score
                    if docid in query_result:  # this document has already been scored once
                        query_result[docid] += score
                    else:
                        query_result[docid] = score
        # need to check about semantic treatment


        sorted_query_result = sorted(query_result.items(), key=lambda x: x[1],reverse=True)
        ans= []
        for i in range(0,min(50,len(sorted_query_result))):
            ans.append(sorted_query_result[i][0])
        return ans

    def read_term_postinglist(self, doc_dict, term):

        if term.lower() in self.dictionary: term=term.lower()
        elif term.upper() in self.dictionary: term=term.upper()
        dictionary_element=self.dictionary[term]
        with open(self.posting_path+"/"+dictionary_element.posting_file,"r") as fin:
            fin.seek(dictionary_element.pointer)
            line= fin.readline()
            posting=line.split(':')[1].split()

            for element in posting:
                tmp=element.split('[')
                doc_num= tmp[0][:-1]
                tmp=tmp[1].split(']')
                freq=len(tmp[0].split(','))
                title=tmp[1].replace(',','')
                doc_dict[doc_num]=[freq,1 if title=="T" else 0]


        return doc_dict
