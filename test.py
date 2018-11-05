import nltk
import  Parse
# r = Reader.ReadFile("D:\iretrival\corpus")

# r.startAction()
# print (nltk.word_tokenize("Twito like bottles in many size and price of 5000$"))
# x="100 3/4 Dollars"
x=Parse.Parser()
#below 1 million
underM =[
"1,890 Dollars",
"450 56/90 Dollars",
"$559,000"]

upM= [
"23,000,000 Dollars",
"$23,987,000",
"$1.89 million",
"$55 billion",
"$1.8 trillion",
"9 m Dollars",
"1.76 bn Dollars",
"6 billion U.S. dollars",
"1.55 million U.S. dollars",
"0.7 trillion U.S. dollars"
]

print("UNDER 1M\n")
for t in underM:
    if t[0]=="$":
        o=True
    else:
        o=False
    i,tt=x.calcPrice(t.replace("$","").split(),0, o)
    print("original value "+t+" ==> "+tt)

print("UP 1M\n")
for t in upM:
    if t[0] == "$":
        o = True
    else:
        o = False
    i,tt=x.calcPrice(t.replace("$","").split(),0,o )
    print("original value "+t+" ==> "+tt)

# y=nltk.word_tokenize("1,000,400")
# print(y)
# z= ["12.34", "1.4","100","1,000","1000","76,023,000,000" , "13,000,000","10,764","1010.98","75.4 thousand","55 thousand","55 million","34 billion",
    # "1.5 trillion","7 Trillion","0.4 billion","0.24 trillion","1.5 billion","130 3/5", "1 32/99","1000500","98000000123"]
# with open("FB396001","r") as fin:
    # x=fin.read()
# t= time.time()
# # x.replace(",", " ").replace("%"," ").replace("("," ").replace(")"," ").replace(":"," ").replace("\""," ").split()
# re.split("[, \-!()$%#@&?:]+", x)
# print(time.time()-t)
# w=[]
# for t in z:
#     yy=nltk.word_tokenize(t)
#     i, term = x.calcSize(yy, 0)
#     w.append(term)
# df = pandas.DataFrame({"original value ":z,"calcsize value":w})
# print(df)