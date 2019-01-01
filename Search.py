import Parse
from Rank import Ranker



class Searcher:

    def __init__(self, queries, dictionary, documents, avgl, posting_path, parser):
        self.queries = queries
        self.ranker = Ranker()
        self.dictionary = dictionary
        self.documents = documents
        self.avgl = avgl
        self.posting_path = posting_path
        self.parser = parser

    def run(self, city_choice,stem):
        """
        This function runs the all given queries
        :param city_choice: list of cities to filter
        :param stem: determines whether do stemming or not
        :return: dictionary - key: queryId, value: list of 50 documents rank in descending order
        """
        results = dict()
        for query_num in self.queries.keys():
            results[query_num] = self.run_query(self.queries[query_num], city_choice,stem)

        # need to return the top 50 documents
        return results

    def run_query(self, query, city_choice, stem):
        """
        This function runs the given query.
        The way of ranking the relevant documents is by BM25 formula.

        :param query: given query content
        :param city_choice:
        :param stem:
        :return: list of the top 50 relevant documents
        """
        query_result = dict()
        query_terms, _ = self.parser.parse(query, stem)
        for term in query_terms:
            doc_dict = dict()
            if term.lower() in self.dictionary or term.upper() in self.dictionary:
                self.read_term_postinglist(doc_dict, term)  # retrieve index entry
                for docid in doc_dict:  # for each document and its word frequency
                    #check whether to filter by city
                    if len(city_choice) > 0:
                        city = self.documents[docid][1]
                        if city not in city_choice:
                            continue
                    score = self.ranker.score_BM25(n=len(doc_dict), f=doc_dict[docid][0], N=len(self.documents),
                                                   dl=self.documents[docid][0],
                                                   avgl=self.avgl, cf=len(query_terms[term].locations),
                                                   title=doc_dict[docid][1])  # calculate score
                    if docid in query_result:  # this document has already been scored once
                        query_result[docid] += score
                    else:
                        query_result[docid] = score
        #sort the documents by they rank descending
        sorted_query_result = sorted(query_result.items(), key=lambda x: x[1], reverse=True)
        ans = []
        #generate list of the top 50 relevant documents
        for i in range(0, min(50, len(sorted_query_result))):
            ans.append(sorted_query_result[i][0])
            i += 1

        return ans

    def read_term_postinglist(self, doc_dict, term):
        """
        This function reads the documents list of the given term from the posting list
        :param doc_dict:
        :param term: given term to read from posting list
        :return: dictionary- key: docNum , value: details about the term(tf,title,locations)
        """

        if term.lower() in self.dictionary:
            term = term.lower()
        elif term.upper() in self.dictionary:
            term = term.upper()
        dictionary_element = self.dictionary[term]
        with open(self.posting_path + "/" + dictionary_element.posting_file, "r") as fin:
            #move the cursor to term location on posting file
            fin.seek(dictionary_element.pointer)
            line = fin.readline()
            posting = line.split(':')[1].split()

            #extract the details from posting elements list
            for element in posting:
                tmp = element.split('[')
                doc_num = tmp[0][:-1]
                tmp = tmp[1].split(']')
                freq = len(tmp[0].split(','))
                title = tmp[1].replace(',', '')
                doc_dict[doc_num] = [freq, 1 if title == "T" else 0]

        return doc_dict
