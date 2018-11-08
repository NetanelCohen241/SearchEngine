import nltk
import time
import re
from lxml.etree import fromstring
import lxml
import  Parse
import spacy
from lxml import etree
from bs4 import BeautifulSoup

x=Parse.Parser()
underM =[
"$400"
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
for i in upM:
      x.parse(i)
for i in underM:
      x.parse(i)








