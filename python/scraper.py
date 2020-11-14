"""
Handler For Loading and Deploying Scrapers
"""
import python.globals as globals

import requests
from bs4 import BeautifulSoup

class ScraperClass():
	_scrapersdb = {}
	_file_urls = []
	_explore_urls = []
	def __init__(self):
		"""
		Loads and Initlizes the scrapers into Memory.
		"""
		for each in globals.databaseRef.pull_scrapers():
			print(each)
			
	def scrape(self, URL):
		print(URL.split('/'))
		if URL.split('/')[2] in self._scrapersdb.keys():
			print("Found Scraper")
			globals.log_write.write("Found Scraper " + URL.split('/')[2] + " ScrapersDB")
		else:
			print("Scraper Does not exist for", URL.split('/')[2])
			globals.log_write.write("Scraper Does Not Exist " + URL.split('/')[2] + " ScrapersDB")
			
	def create_scraper(self, URL)
		
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, 'html.parser')
		
		user = ''
		while user != "quit"
			print(soup.user)
			user = input("User Input: ")
