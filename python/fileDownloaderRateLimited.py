import requests

from ratelimiter import RateLimiter
from PIL import Image
import hashlib

import python.globals as universal


class InternetHandler():
    _pics = {}
    _spider = []
    _filename = {}
    def __init__(self, user_agent, rate_limit, URL):
        self.user_agent = user_agent
        self.rate_limit = rate_limit
        self._spider.append(URL)
	    
        self.rate_limiter = RateLimiter(max_calls=self.rate_limit, period=5, callback=self.limit)

	    
    def limit(until, *args):
        print("Rate Limited for ", until, *args)
	    
    def request_data(self):
        #universal.scraper_store[self.URL.split('/')[2]]
        #print("file", universal.scraper_store)
        with self.rate_limiter:
            page = requests.get(self._spider[-1], headers = {'User-Agent': self.user_agent})
            parsed_data = universal.scraperHandler.run_scraper(str(universal.scraper_store[self._spider[-1].split('/')[2]]), self._spider[-1], page)
	        
            for each in parsed_data.keys():
                print(parsed_data[each])
                self._pics[parsed_data[each]["id"]] = parsed_data[each]["pic"]
                self._filename[parsed_data[each]["id"]] = parsed_data[each]["filename"]
            #print("Pics", self._pics)
            self.download_pic()

    def hash256(self, image_ref):
        file_hash = hashlib.sha256()
        for data in image_ref.iter_content(8192):
             file_hash.update(data)
        #file_hash.update(image_ref)
        print(file_hash.hexdigest())

    def download_pic(self):
    
        # NEEDS TO BE IN THIS ORDER FOR RATE LIMITING TO WORK PROPERLY
        for each in self._pics.keys():
            with self.rate_limiter:
            
                file_hash = hashlib.sha256()
                # Code shamelessly stolen from:
                # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
                with requests.get(self._pics[each]) as r:
                    r.raise_for_status()

                
                    #r.raise_for_status()
                    self.hash256(r)
                    r.raw.decode_content = False
                    
                    with open(self._filename[each], 'wb') as fileTemp:
                        for chunk in r.iter_content(chunk_size=8192):
                            fileTemp.write(chunk)
                
