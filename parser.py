import docx
from PyPDF2 import PdfFileReader
import os

class RawText:
    def __init__(self, location):
        self.contents = [] # make this a dict key should be type+#
        self.wtf(location)

    def wtf(self, location):
        # divide location string, let's work with windows
        file = location.split('/')
        fin = len(file) - 1

        # find the TYPE
        name = file[fin].split('.')
        matype = name[len(name) - 1]

        if matype in ('doc', 'docx'):
            self.wordreader(location)
        elif matype == "pdf" :
            self.pdfreader(location)
        else:
            self.otherreader()

    def wordreader(self,location):
        word = docx.Document(location)

        for p in word.paragraphs:
            self.contents.append(p.text)

    def pdfreader(self,location):
        pdf = PdfFileReader(open(location, "rb"))
        length = pdf.numPages

        for i in range(0,length):
            self.contents.append(pdf.getPage(i).extractText())

    def otherreader(self):
        print("I was made by a bad programmer")


if __name__ == "__main__":
    PATH = os.getcwd()
    x = RawText(PATH+"\\1Resume.docx")
    print(x.contents)