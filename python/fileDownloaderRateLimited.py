import requests

from ratelimiter import RateLimiter
from PIL import Image
import hashlib
import os

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
	        # TODO Implement database intersection. Remove allready in database from to parse.
            for each in parsed_data.keys():
                #print(parsed_data[each])
                self._pics[parsed_data[each]["id"]] = parsed_data[each]["pic"]
                self._filename[parsed_data[each]["id"]] = parsed_data[each]["filename"]
            #print("Pics", self._pics)
            return self.download_pic(), parsed_data
            
            
            
            
            

    def hash256(self, image_ref):
        file_hash = hashlib.sha256()
        for data in image_ref.iter_content(8192):
             file_hash.update(data)
        #file_hash.update(image_ref)
        print(file_hash.hexdigest())
        return file_hash.hexdigest()
        
    def check_dir(self, hash_input):
        hone = ''
        htwo = ''
        hone = str(hash_input)[0] + str(hash_input)[1] + '/'
        htwo = str(hash_input)[2] + str(hash_input)[3] + '/'

        databaseloc = universal.databaseRef.pull_data("Settings", "name", "FilesLoc")[0][3]


        if not os.path.isdir(universal.db_dir + databaseloc + hone):
            os.mkdir(universal.db_dir + databaseloc + hone)
        if not os.path.isdir(universal.db_dir + databaseloc + hone + htwo):
            os.mkdir(universal.db_dir + databaseloc + hone + htwo)
        #print(hone, htwo)
        
        return universal.db_dir + databaseloc + hone + htwo

    def download_pic(self):
        
        formattedData = {}
        
        # NEEDS TO BE IN THIS ORDER FOR RATE LIMITING TO WORK PROPERLY
        for each in self._pics.keys():
            individualData = []
            with self.rate_limiter:
            
                file_hash = hashlib.sha256()
                # Code shamelessly stolen from:
                # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
                with requests.get(self._pics[each]) as r:
                    r.raise_for_status()

                
                    #r.raise_for_status()
                    image_hash = self.hash256(r)
                    r.raw.decode_content = False
                    
                    filepath = self.check_dir(image_hash)
                    
                    with open(filepath + self._filename[each], 'wb') as fileTemp:
                        for chunk in r.iter_content(chunk_size=8192):
                            fileTemp.write(chunk)

                individualData.append(self._filename[each])
                individualData.append(image_hash)
            
            formattedData[each] = individualData
        return formattedData
