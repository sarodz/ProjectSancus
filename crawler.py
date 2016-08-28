# !/bin/usr/python
import operator
import os
import pandas as pd
import requests
import sys
import time
import unidecode
import unicodecsv as csv

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from string import punctuation
from selenium import webdriver

# import webbrowser
PATH = os.getcwd() #Get Current Working Directory

def main(path):
	login(path)#logs into a job search website. Need error handling for the case for already have logged in
	inputAnswer=raw_input("How many pages would you like to search?") #Need error handling for not inputting number
	crawler(inputAnswer) #crawler goes through an already logged in website's search motor
	
#The login function should include more websites later on	
def login(path):
	# Get login form
	URL = 'https://www.linkedin.com/uas/login'
	session = requests.session()
	login_response = session.get('https://www.linkedin.com/uas/login')
	login = BeautifulSoup(login_response.text)

	# Get hidden form inputs
	inputs = login.find('form', {'name': 'login'}).findAll('input', {'type': ['hidden', 'submit']})

	# Create POST data
	post = {input.get('name'): input.get('value') for input in inputs}
	post['session_key'] = 'username'
	post['session_password'] = 'password'

	# Post login
	post_response = session.post('https://www.linkedin.com/uas/login-submit', data=post)

	# Get home page
	home_response = session.get('http://www.linkedin.com/nhome')
	home = BeautifulSoup(home_response.text)
		
		
	
		
		
#The crawler, currently works only for linkedIn, but this can be (and should be) changed to include other sites
def crawler(max_page):
	start = 0	#Shows the first X results on a page
	page = 1	#Shows which page we are in
	while page <= int(max_page):
		keywords = sys.argv[1:-1]
		search_term = '+'.join(keywords)
		#Next steps: Have multiple website url adaptations
		#Location Id is a bit annoying, set it to default. The function needs to take location as an input
		url = 'http://in.linkedin.com/jobs/search?keywords=' + str(search_term) + '&locationId=in:0&start=' + str(start) + '&count=25&trk=jobs_jserp_pagination_' + str(page)
		source = requests.get(url)
		text = source.text
		to_crawl = BeautifulSoup(text)
		print page
		print start
		
		job_title = to_crawl.findAll('a', {'class': 'job-title-link'})
		company_name = to_crawl.findAll('span', {'class': 'company-name-text'})
		location = to_crawl.findAll('span', {'itemprop': 'addressLocality'})
		for link1, link2, link3 in zip(job_title, company_name, location):
			href = link1.get('href')
			print link1.text
			print href
			print link2.text
			print link3.text
			print '\n'

		page += 1
		start += 25

if __name__ == "__main__":
	main() #Bak headquarters degil, adam gibi main. Bak da ogren hippi
