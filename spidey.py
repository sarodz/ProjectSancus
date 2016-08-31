from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse
import requests
from bs4 import BeautifulSoup
import re

class LinkParser(HTMLParser):
    """Generates links for major job posting sites and collects job information

        Attributes:
            location (str): The location of the job search
            topic (str): The type of jobs crawler looks at
            link (str): For cases the user provides a link [revise]
            limit (int): Limit search
    """
    def __init__(self, location, topic, link = None, limit = 0):
        self.limit = limit
        _, self.link = self.getLinks(link) #let's divy this to a link checker and a data returner
        self.location = location
        self.topic = topic

    def indeedURL(self):
        """Helper function to create the URL for Indeed
        :return: String url needed for the search
        """
        page = 0 #increment by 20 (self.limit*20 ?)
        # format page to match what Indeed is looking for
        search_term = re.sub(' ', '+', self.topic)
        # generic Indeed link
        url = 'http://www.indeed.ca/jobs?q=' + str(search_term) + '&l=' + self.location + '&start=' + str(page)

        # Collect & return HTML -- We can either have multiple crawlers OR
        # multiple helper functions to create URLs.
        #source = requests.get(url)
        #text = source.text
        #to_crawl = BeautifulSoup(text, 'lxml')

        return url

    def monsterURL(self):
        """Helper function to create the URL for Monster
        :return: String url needed for the search
        """
        page = 1 #increment by +1
        # format page to match what Monster is looking for
        search_term = re.sub(' ', '-', self.topic)
        # generic Monster link
        url = 'http://www.monster.ca/jobs?q=' + str(search_term) + '&where=' + self.location + '&page=' + str(page)

        return url

    def wpolisURL(self):
        """Helper function to create the URL for Workopolis
        :return: String url needed for the search
        """
        page = 1 #increment by +1
        # format page to match what Monster is looking for
        search_term = re.sub(' ', '+', self.topic)
        # generic Monster link
        url = 'http://www.workopolis.com/jobsearch/find-jobs?lg=en&ak=' + str(search_term) + '&l=' + self.location + '&pn=' + str(page)

        return url

    def handle_starttag(self, tag, attrs):
        """Generic URL handler
        """
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
    # DIVY THE FUNCTION (?) FOR SANITY CHECK
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