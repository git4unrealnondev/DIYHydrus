"""
Handler For Loading and Deploying Scrapers
"""
import python.globals as universal

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
        for each in universal.databaseRef.pull_scrapers():
            print(each)

    def scrape(self, URL):
        ''' Checks to see if scraper exists and if it doesn't it will prompt the user to create one. '''
        if URL.split('/')[2] in self._scrapersdb.keys():
            print("Found Scraper")
            universal.log_write.write("Found Scraper " + URL.split('/')[2] + " ScrapersDB")
        else:
            print("Scraper Does not exist for", URL.split('/')[2])
            universal.log_write.write("Scraper Does Not Exist " + URL.split('/')[2] + " ScrapersDB")

            # Loops Through to get correct user input, y or n
            while True:
                print("Create Scraper for " + str(URL.split('/')[2]) + "?")
                user_input = input("y or n: ")

                if user_input.upper() == "Y":
                    universal.log_write.write("User is creating Scraper for" + str(URL.split('/')[2]) + ".")
                    #self.create_scraper(URL)
                    test = "print(URL)"
					
                    exec(test, {"URL": URL})
                    break
                elif user_input.upper() == "N":
                    universal.log_write.write("User has decided to not create a scraper.")
                    break
    def run_scraper(self, *args):
		'''
		Runs Scraper from memory
		'''
		if len(args) >= 2:
			scriptString = args[0]
			URL = args[1]

		elif len(args) == 1:
			scriptString = args[0]
			print("I Need the URL for the scraper to work")
			URL = input(": ")
		
		else:
			print ("A Stupid Code error has happened in run_scraper.")
			universal.log_write.write("A Stupid Code error has happened in run_scraper.")
			universal.log_write.write("DEBUG AS FOLLOWS")
			universal.log_write.write(args)
			
		# Initing a passthrough Variable
		loc = {}
		exec(scriptString, {"URL": URL, "json": globals}, loc)
		return_data = loc['return_json']
		print(return_data)
	def replace_scraper(self, scraper_file):
		'''
		Reads Scraper into Memory
		'''
		scriptString = ""

		#Reads script into memory
		with open(scraper_file, "r") as infile:
			for each in infile:
				scriptString += each + "\n"

		#Executes Script
		self.run_scraper(scriptString)

	'''def create_scraper(self, URL):
		
		print("Enter Custom User Agent")
		print("IE: DIYHydrus/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 DIYHydrus/10.0")
		header = input(": ")
		page = requests.get(URL, headers = {'User-Agent': header})
		soup = BeautifulSoup(page.content, 'html.parser')
		
		user = ''
		while user != "quit":
			#print (soup)
			print(user)
			user = input("User Input: ")'''
