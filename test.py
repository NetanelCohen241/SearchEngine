import Reader
import nltk
# r = Reader.ReadFile("D:\iretrival\corpus")
import  Parse
import pandas
import nltk
# r = Reader.ReadFile("D:\iretrival\corpus")

# r.startAction()
# print (nltk.word_tokenize("Twito like bottles in many size and price of 5000$"))
print (nltk.word_tokenize("100 3/4 Dollars"))
x=Parse.Parser()
# y=nltk.word_tokenize("1,000,400")
# print(y)
# print (x.calcSize(y,0))

z= ["12.34", "1.4","100","1,000","1000","76,023,000,000" , "13,000,000","10,764","1010.98","75.4 thousand","55 thousand","55 million","34 billion",
    "1.5 trillion","7 Trillion","0.4 billion","0.24 trillion","1.5 billion","130 3/5", "1 32/99","1000500","98000000123"]
w=[]
for t in z:
    yy=nltk.word_tokenize(t)
    i, term = x.calcSize(yy, 0)
    w.append(term)
df = pandas.DataFrame({"original value ":z,"calcsize value":w})
print(df)