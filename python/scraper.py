"""
Handler For Loading and Deploying Scrapers
"""
import python.globals as universal

import json
import requests
from bs4 import BeautifulSoup

class ScraperClass():

    scraper_rate_limited = None

    def __init__(self):
        """
        Loads and Initlizes the scrapers into Memory.
        """
        for each in universal.databaseRef.pull_scrapers():
            print(each)
            self.scraper_list_handler(each)
        
        # Adding a scraper list for rate limiting
        universal.scraper_list = {}
        universal.scraper_store = {}

    def __del__(self):
        if not self.scraper_rate_limited is None:
            downloadedFiles, parsed_data = self.scraper_rate_limited.removal()
            # Interprets and prepares data for database.
            self.interpret_data(parsed_data, downloadedFiles)
            #for each in universal.scraper_store:
            #    each.removal()

    def scrape(self, URL):
        ''' Checks to see if scraper exists and if it doesn't it will prompt the user to create one. '''
        if URL.split('/')[2] in universal.scraper_list.keys():
            print("Found Scraper", URL.split('/')[2])
            #print("keys", universal.scraper_list.keys(), URL.split('/')[2])
            universal.log_write.write("Found Scraper " + URL.split('/')[2] + " ScrapersDB")
            
            # Pulling ratelimited INSTANCE TO BE USED
            self.scraper_rate_limited = universal.scraper_list[URL.split('/')[2]]
            
            # TODO Potential INSERTION point for files already in DB
            downloadedFiles, parsed_data = self.scraper_rate_limited.request_data()
            
            # downloadedFiles contains filename & sha256 hash
            for each in downloadedFiles:
                print(each)
            
            for each in parsed_data.keys():
                print(parsed_data[each])
                
            # Interprets and prepares data for database.
            self.interpret_data(parsed_data, downloadedFiles)

        ''' 
        else: # OLD CODE POTENTIALLY DELETE
            print("BADCODE AHEAD DO NOT USE")
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
                    break'''

    def interpret_data(self, data, file_data):
    

    
        for each in data.keys():

            universal.databaseRef.file_manager(file_data[each][1], file_data[each][0], None, file_data[each][0].split('.')[1])

            for every in data[each]:
            
                universal.databaseRef.namespace_manager(every)
            
                if type(data[each][every]) is list:
                    for ec in data[each][every]:
                        #print("List", ec)
                        #print('1')
                        universal.databaseRef.tag_namespace_manager(ec, every)
                        
                        universal.databaseRef.t_and_f_relation_manager(file_data[each][1], ec)

                        
                if type(data[each][every]) is dict:
                    for ec in data[each][every].keys():
                        #print('2')
                        universal.databaseRef.tag_namespace_manager(ec, every)
                        
                        universal.databaseRef.t_and_f_relation_manager(file_data[each][1], ec)

                        #print("Dict", ec, data[each][every][ec])
                if type(data[each][every]) is str:
                    #print(data[each][every])
                    #print("every", every, data[each][every])
                    #print('3')
                    universal.databaseRef.tag_namespace_manager(data[each][every], every)
                    
                    universal.databaseRef.t_and_f_relation_manager(file_data[each][1], data[each][every])

                    
                if type(data[each][every]) is int:
                    
                    #print("every", every, data[each][every])
                    universal.databaseRef.tag_namespace_manager(data[each][every], every)
                    #print('4')
                    #print(every, data[each][every])
                    universal.databaseRef.t_and_f_relation_manager(file_data[each][1], data[each][every])
                

                #print(every ,data[each][every])
                
        universal.databaseRef.write()
        
    def scraper_list_handler(self, scraper_name, pulled_data, URL):
        '''
        Handles scraper objects for rate limiting.
        Adds pulled data into scraper from script pulled data.
        '''
        if "USER_AGENT" in pulled_data.keys():
            user_agent = pulled_data["USER_AGENT"]
        else:
            print("COULD NOT FIND USER_AGENT IN", scraper_name, "!", " DEFAULTING TO DB DEFAULT!")
            universal.log_write.write("COULD NOT FIND USER_AGENT IN " + scraper_name + "!" + " DEFAULTING TO DB DEFAULT.")
            user_agent = universal.databaseRef.pull_data("Settings", "name", "DEFAULTUSERAGENT")[0][3]
        if "RATE_LIMIT" in pulled_data.keys():
            rate_limit = pulled_data["RATE_LIMIT"]
        else:
            print("COULD NOT FIND RATE_LIMIT IN", scraper_name, "!", " DEFAULTING TO DB DEFAULT!")
            universal.log_write.write("COULD NOT FIND RATE_LIMIT IN " + scraper_name + "!" + " DEFAULTING TO DB DEFAULT.")
            rate_limit = universal.databaseRef.pull_data("Settings", "name", "DEFAULTRATELIMIT")[0][2]
        print("Parsed Data", "USERAGENT:",user_agent, "RATELIMIT:",rate_limit)
        
        if scraper_name in universal.scraper_list.keys():
            return universal.scraper_list[scraper_name]
        else:
            # Scraper is not in list need to create a new one and append to scraper list.
            universal.scraper_list[scraper_name] = universal.rateLimiter.InternetHandler(user_agent, rate_limit, URL)
            return universal.scraper_list[scraper_name]

    def run_scraper(self, *args):
        '''
        Runs Scraper from memory
        Reads variables from script into new fileDownloader instance &
        Adds new fileDownloader into universal.scraper_list w/
        the name being the websites URL and the fileDownloader as its value.
        
        args[0] is the script thats loaded into memory
        args[1] is the URL thats will be scraped
        args[2] is the web_data pulled from fileDownloader
        '''
        # Detecting if URL has been passed into scraper
        if not args[1] is None:
            scriptString = args[0]
            URL = args[1]

        # URL HAS NOT been passed into scraper
        elif args[1] is None:
            scriptString = args[0]
            print("I Need the URL for the scraper to work")
            URL = input(": ")
		
        else:
            print ("A Stupid Code error has happened in run_scraper.")
            universal.log_write.write("A Stupid Code error has happened in run_scraper.")
            universal.log_write.write("DEBUG AS FOLLOWS")
            universal.log_write.write(args)

        # Initing a passthrough Variable
        # loc contains ALL VARIABLES & FUNCTION CALLS IN SCRIPT
        loc = {}
        if len(args) == 3:
	        exec(scriptString, {"universal": universal, "web_data": args[2]}, loc)
	        #print(loc)
	        return loc['stored_data']
        else:

        
            exec(scriptString, {"universal": universal}, loc)
            
        return_data = loc['stored_data']
        #print("LOC", loc)
        #print(return_data)
        
        # Passes URL to scraper to add to universal.scraper_list
        self.scraper_list_handler(URL.split('/')[2], loc, URL)
        
        print(universal.scraper_list)

    def replace_scraper(self, scraper_file, *args):
        '''
        Reads Scraper into Memory
        '''
        scriptString = ""

        #Reads script into memory
        with open(scraper_file, "r") as infile:
            for each in infile:
                scriptString += each + "\n"

        #Places Script into scraper_store
        universal.scraper_store[args[0].split('/')[2]] = scriptString

        #Executes Script
        self.run_scraper(scriptString, args[0])
    # Ignore me OLD CODE
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
