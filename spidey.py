from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

#LinkParser uses some methods from HTMLParser
class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # Looking for the begining of a link. Links normally look like <a href="www.someurl.com"></a>
        if tag  'a':
            for (key, value) in attrs:
                if key  'href':
                    # Grabbing the new URL. Also adding the
                    # base URL to it. For example:
                    # www.derp.com is the base and
                    # somepage.html is the new URL (a relative URL)
                    #
                    # Combine a relative URL with the base URL to create
                    # an absolute URL like:
                    # www.derp.com/somepage.html
                    newUrl = parse.urljoin(self.baseUrl, value)
                    # And add it to colection of links:
                    self.links = self.links + [newUrl]

    # This is a new function to get links
    # that spider() function will call
    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        # Make sure that we are looking at HTML and not other things that
        # are floating around on the internet (such as
        # JavaScript files, CSS, or .PDFs for example)
        if response.getheader('Content-Type')=='text/html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]

# Spider takes in an URL, a word to find,
# and the number of pages to search through before giving up
def spider(url, word, maxPages):  
    pagesToVisit = [url]
    numberVisited = 0
    foundList = []
	foundListIndex=0;
    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited = numberVisited +1
        # Start from the beginning of our collection of pages to visit:
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            parser = LinkParser()
            data, links = parser.getLinks(url)
            if data.find(word)>-1:
                foundList[i]=url
				i=i+1
                # Add the pages that we visited to the end of our collection
                # of pages to visit:
                pagesToVisit = pagesToVisit + links
                print(" **Success!**")
        except:
            print(" **Failed!**")