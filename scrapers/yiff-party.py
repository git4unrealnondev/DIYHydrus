'''
Scraper that will scrape new yiff party
'''

from bs4 import BeautifulSoup, SoupStrainer
import cfscrape
import re
global re
global BeautifulSoup
global cfscrape
global SoupStrainer


class Func():
    def __init__(self, web_data):
        self.web_data = web_data
        self.scraper = cfscrape.create_scraper()
        self.rate_limiter = self.web_data[0]
        

    def handle(self, init_url):
        '''
        Parses data from site
        '''
        pass


    def web_data_check(self):

        self.init_url = self.web_data[0]
        
        self.parent = self.web_data[2]
        
        base = "https://yiff-party.com"
        search_term = "/?s="
        page_term = "/page/"
        search_spacer = "+"
        
        DEFAULT_PAGE = 1
        page_cnt = DEFAULT_PAGE
        
        parsed_search = self.parent.search_term.replace(" ", search_spacer)
        
        parentURL= base + page_term + str(page_cnt) + search_term + parsed_search
        #https://yiff-party.com/page/2/?s=drawn
        
        if (self.init_url is None):
        
            print(parentURL, self.init_url)
        
            return ""

if 'web_data' in globals():
    print("I am getting called from fileDownloaderRateLimited")
    useless_storage = Func(web_data)
    stored_data = useless_storage.web_data_check()
else:
    print("I am getting called from scraper.py . My variables are getting read.")
    # Empty Pass back for laziness
    stored_data = ''