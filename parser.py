import docx
#import PyPDF2

class Text:
    def __init__(self, location):
        self.wtf(location)

    def wtf(self, location):
        # divide location string, let's work with windows
        file = location.split('/')
        fin = len(file) - 1

        # find the type
        name = file[fin].split('.')
        matype = name[len(name) - 1]

        if matype in ('doc', 'docx'):
            self.wordreader(location)
        elif matype == "pdf" :
            self.pdfreader(location)
        else:
            self.otherreader()

    def wordreader(self,location):
        print("I iz word")

    def pdfreader(self,location):
        print("No fool, I am pdf")

    def otherreader(self):
        print("I was made by a bad programmer")


#def headquarters():
#    print("Fun")

if __name__ == "__main__":
    Text("aa/aa/resume.kk")