import docx
from PyPDF2 import PdfFileReader
import os
import re
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from string import punctuation

class RawText:
    """Collect and organize raw data from user posted content

        Arguments:
            location (str): Insert the location of the file in PC
    """
    def __init__(self, location):
        self.contents = [] # make this a dict (?) key should be type+#
        self.stemmedcontent = self.contents
        self.sorter(location)

    def sorter(self, location):
        # divide location string, let's work with windows
        file = location.split('/')
        fin = len(file) - 1

        # find the TYPE
        name = file[fin].split('.')
        matype = name[len(name) - 1]

        if matype == 'docx':
            self.wordreader(location, matype)
        elif matype == "pdf":
            self.pdfreader(location)
        elif matype == "txt":
            self.txtreader(location)
        else:
            self.throw_error()

    def wordreader(self,location):
        word = docx.Document(location)

        for p in word.paragraphs:
            self.contents.append(p.text)

    def pdfreader(self,location):
        pdf = PdfFileReader(open(location, "rb"))
        length = pdf.numPages

        for i in range(0,length):
            page = pdf.getPage(i).extractText()
            page = re.sub('\n', '', page)
            self.contents.append(page)

    def txtreader(self, location):
        with open(location, 'r') as f:
            self.contents.append(f.read())

    def throw_error(self):
        print("This type is not supported. Please use pdf, docx or txt.")
        # maybe we can create a loger to check what went wrong?

    # REWRITE!
    def stem_it(self):
        stemmer = SnowballStemmer("english")
        data = self.contents
        merged = []
        sw = stopwords.words("english")

        tokenized = [word_tokenize(c) for c in data]
        for i in range(0, len(tokenized)):
            merged = merged + tokenized[i]
        for i in range(0, len(merged)):
            self.stemmedcontent.append(stemmer.stem(merged[i]))

        self.stemmedcontent = [word for word in self.stemmedcontent if word not in sw and word not in punctuation]

        return self.stemmedcontent

    #TO DO: __str__ function to pretify, Map/Reduce (?)

if __name__ == "__main__":
    PATH = os.getcwd()
    i = RawText(PATH+"\Office job - CoverLetter.pdf")
    print(i.stem_it())