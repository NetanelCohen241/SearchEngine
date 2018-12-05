import os
import linecache
import heapq
from nltk.stem.snowball import EnglishStemmer


class MyHeap(object):
    def __init__(self, initial=None, key=lambda x: x):
        self.key = key
        if initial:
            self._data = [(key(item[0]), item) for item in initial]
            heapq.heapify(self._data)
        else:
            self._data = []

    def push(self, item):
        heapq.heappush(self._data, (self.key(item[0]), item))

    def pop(self):
        return heapq.heappop(self._data)[1]

    def peek(self, i):
        if len(self._data) == 0:
            return ["", -1]
        else:
            return self._data[i][1]


class DictionaryElement(object):
    def __init__(self, posting_file):
        self.posting_file = posting_file
        self.corpus_tf = 0
        self.pointer = 0

    def to_string(self):
        return self.posting_file + "," + str(self.pointer) + "," + str(self.corpus_tf)


class Merger(object):
    def __init__(self, files_to_merge_path, chunk_size):

        self.files_to_merge_path = files_to_merge_path
        self.chunk_size = chunk_size
        self.dictionary = {}
        self.posting_block = {}
        self.chunks_list_to_merge = []
        self.pointers = []
        self.files_names = []
        self.file_name = ""

    def merge(self, file_name):
        """
        This function merge the files into one sorted file - posting list
        :return:
        """
        # if not os.path.isfile(self.files_to_merge_path + "/dictionary.txt"):
        open(self.files_to_merge_path + "/dictionary" + file_name[7:] + ".txt", "w+")
        self.file_name = file_name
        self.files_names = [word for word in os.listdir(os.getcwd()) if word.startswith(file_name)]
        terms = []
        self.upload_all_files_chunks()
        # insert into terms list the first term from each chunk
        for i in range(0, len(self.chunks_list_to_merge)):
            terms.append([self.chunks_list_to_merge[i][0][self.pointers[i]], i])

        self.start_merge(terms)
        self.write_dictionary_to_disk(file_name)
        self.__remove_tmp_files(file_name)

    def start_merge(self, terms):
        """
        This function implements the merge process.
        Upload the all files in chunks.
        Iterate over the all chunks.( Each chunk is sorted)
        The merge: find the minimum value among the all chunks, merge the minimum value content for each file that the minimum is in it.
        Save the merged data into class member postingBlock(dictionary)
        And so on ,until we upload the all chunks.
        :param terms:
        :return:
        """
        terms = MyHeap(terms, str.lower)
        posting_list_pointer = 0
        posting_id = 1
        while not self.has_finished():

            term, merge_content = self.next_term(terms)

            self.posting_block[term] = merge_content
            total_freq = self.__calculate_total_tf(merge_content)
            self.__add_to_dictionary(term, "posting" + str(posting_id) + ".txt", posting_list_pointer, total_freq)
            posting_list_pointer += len(term) + len(merge_content) + 3

            if posting_list_pointer > 200000000:
                self.__write_merge_content_to_disk(self.file_name + str(posting_id) + ".txt")
                posting_id += 1
                posting_list_pointer = 0
        self.__write_merge_content_to_disk(self.file_name + str(posting_id) + ".txt")

    def next_term(self, terms):
        """
        This function dequeue terms from as long as its the same term(ignore case)
        :param terms: priority queue of terms ordered by ascii
        :return: the term and its posting list
        """
        next = ""
        merge = ""
        term = ""
        is_lower = False

        while not self.has_finished() and term.lower() == next.lower():
            min_term = terms.pop()
            t = min_term[0]
            if self.dictionary.__contains__(t):
                print("5")
            min_idx = min_term[1]
            pos = self.pointers[min_idx] % self.chunk_size
            merge += " " + self.chunks_list_to_merge[min_idx][1][pos].replace('\n', "")

            if not is_lower:
                if t.islower() or t[0].islower():
                    term = t
                    is_lower = True
                elif t[0].isupper():
                    term = t.upper()
                else:
                    term = t

            self.pointers[min_idx] += 1
            if self.pointers[min_idx] % self.chunk_size == 0:
                self.upload_file_chunk(min_idx)
            if self.pointers[min_idx] != -1:
                terms.push([self.chunks_list_to_merge[min_idx][0][self.pointers[min_idx] % self.chunk_size], min_idx])
            next = terms.peek(0)[0]

        return term, merge

    def upload_all_files_chunks(self):
        """
        This function upload chunk(of lines) from each file(postinglist
        :return:
        """
        for i in range(len(self.files_names)):
            self.chunks_list_to_merge.append(0)
            self.pointers.append(0)
            self.upload_file_chunk(i)

    def upload_file_chunk(self, file_number):

        term_dict = self.read_lines(file_number, self.pointers[file_number], self.chunk_size)
        self.chunks_list_to_merge[file_number] = term_dict

    def read_lines(self, file_number, start, how_many_to_read):
        """
        This function read specific lines from a file.
        :param file_number:
        :param start: from which line start to read
        :param how_many_to_read:
        :return: dictionary
        """
        file_name = self.files_names[file_number]
        keys = []
        values = []
        if start < 0: return ''
        current_line_number = start
        eof = True
        for i in range(start, start + how_many_to_read):
            line = linecache.getline(file_name, i + 1)
            if line == "":
                break
            tmp = line.split(':')
            keys.append(tmp[0])
            values.append(tmp[1].replace('\n', ''))
            eof = False
            current_line_number += 1

        if eof:
            self.pointers[file_number] = -1
            return [[""], [""]]
        if current_line_number != start + how_many_to_read:
            for i in range(0, how_many_to_read + start - current_line_number):
                keys.insert(0, "")
                values.insert(0, "")
            self.pointers[file_number] = how_many_to_read + start - (current_line_number % how_many_to_read)

        return [keys, values]

    def has_finished(self):

        ans = True
        for i in range(len(self.pointers)):
            if self.pointers[i] != -1:
                ans = False
                break
        return ans

    def __write_merge_content_to_disk(self, file_name):
        """
        This function writes the posting list into the disc
        :return:
        """
        with open(self.files_to_merge_path + "/" + file_name, "w+") as out:
            for key in self.posting_block.keys():
                out.write(key + ":")
                out.write(self.posting_block[key] + '\n')
        out.close()
        self.posting_block = {}

    def write_dictionary_to_disk(self, file_name):
        """
        This function writes the dictionary into the disc
        :return:
        """
        with open(self.files_to_merge_path + "/dictionary" + file_name[7:] + ".txt", "w+") as out:
            for key in self.dictionary.keys():
                out.write(key + ":")
                out.write(self.dictionary[key].to_string() + '\n')
        out.close()

    def __add_to_dictionary(self, term, posting_file, posting_list_pointer, tf):

        e = DictionaryElement(posting_file)
        e.pointer = posting_list_pointer
        e.corpus_tf = tf
        self.dictionary[term] = e

    def __calculate_total_tf(self, line):

        term_corpus_frequency = 0
        try:
            elements = line.split()
            for i in range(len(elements)):
                term_corpus_frequency += len(elements[i].split('[')[1].split(','))
        except:
            return 0
        return term_corpus_frequency

    def upload_dictionary(self, stem):
        try:
            with open(self.files_to_merge_path + "/dictionary" + stem + ".txt", "r")as out:
                lines = out.readlines()
                for line in lines:
                    l = line.split(":")
                    pos = l[1].split(",")
                    e = DictionaryElement(pos[0])
                    e.pointer = int(pos[1])
                    e.corpus_tf = int(pos[2])
                    self.dictionary[l[0]] = e
            out.close()
        except:
            print("task to upload dictionary failed successfully")
        return self.dictionary

    def city_index(self):

        city_files = [word for word in os.listdir(os.getcwd()) if word.startswith("city")]
        cities = {}
        e = EnglishStemmer()
        # build cities dictionary
        for i in range(len(city_files)):
            with open(city_files[i], "r") as c:
                lines = c.readlines()
                for line in lines:
                    city = line.split(":")
                    if not cities.__contains__(city[0]):
                        try:
                            if "Stem" in self.file_name:
                                city[0] = e.stem(city[0])
                            if self.dictionary.__contains__(city[0].upper()):
                                cities[city[0]] = city[1].replace('\n', '') + " " + str(
                                    self.dictionary[city[0].upper()].posting_file) \
                                                  + "," + str(self.dictionary[city[0].upper()].pointer)
                            else:
                                cities[city[0]] = city[1].replace('\n', '') + " " + str(
                                    self.dictionary[city[0].lower()].posting_file) \
                                                  + "," + str(self.dictionary[city[0].lower()].pointer)
                        except:
                            x = i
                            print(str(i) + "    " + city[0])

        # write cities to disk
        with open(self.files_to_merge_path + "/cities.txt", "w+") as c:
            for city in cities:
                c.write(city + ": " + cities[city] + '\n')
            c.close()
            self.__remove_tmp_files("city")

    def language_index(self):

        line = "."
        i = 1
        language = {}
        while line != "":
            line = linecache.getline("language.txt", i).split()
            if len(line) == 0 or line[0].isdigit():
                break
            line = line[0].replace(',', '').lower()
            if not language.__contains__(line):
                language[line] = ""
            i += 1

        with open(self.files_to_merge_path + "/languages.txt", "w+")as out:
            for key in language:
                out.write(key + '\n')
        out.close()
        self.__remove_tmp_files("language.txt")

    def __remove_tmp_files(self, file_name):

        files = [word for word in os.listdir(os.getcwd()) if word.startswith(file_name)]
        for file in files:
            os.remove(file)
