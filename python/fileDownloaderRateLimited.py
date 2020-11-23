import requests

from ratelimiter import RateLimiter
from PIL import Image
import hashlib
import os

import python.globals as universal
import urllib

class InternetHandler():
    _pics = {}
    _spider = []
    _filename = {}
    def __init__(self, user_agent, rate_limit, URL):
        self.user_agent = user_agent
        self.rate_limit = rate_limit
        self._spider.append(URL)
	    
        self.rate_limiter = RateLimiter(max_calls=self.rate_limit, period=5, callback=self.limit)

        self.formattedData = None

    def removal(self):
        '''
        Trims list to hand to scraper for database adding upon untimely close.
        
        '''
        #for each in self.formattedData:
        #print("Parsed_DATA", self.parsed_data)
    
        #print("len", len(self.formattedData), len(self.parsed_data))
    
        data = self.parsed_data
        temp = {}
        
        #print(self.formattedData)
        
        #print(self.parsed_data)

        if self.formattedData is None:
            return None, None

        for each in self.formattedData.keys():
            temp[each] = data[each]
        #print(len(data), len(data) - len(self.formattedData), type(data))
        #print(len(temp))
        return self.formattedData, temp
	    
    def limit(until, *args):
        print("Rate Limited for ", until, *args)
	    
    def request_data(self):
        '''
        Pulls data from website and gets a list of pictures to download.
        '''
        with self.rate_limiter:
            page = requests.get(self._spider[-1], headers = {'User-Agent': self.user_agent})
            self.parsed_data = universal.scraperHandler.run_scraper(str(universal.scraper_store[self._spider[-1].split('/')[2]]), self._spider[-1], page)

            # Function cleans files based on picture source already being inside the DB.
            self.cleaned_data = self.parsed_data.copy()
            for each in self.parsed_data.keys():
                url_list = universal.databaseRef.pull_data("Tags", "name", str(str(urllib.parse.quote(str(self.parsed_data[each]["pic"])))))
                if not url_list == []:
                    del self.cleaned_data[each]
                    print("Not adding", url_list[0][1], "to list to download already in DB.")
                    universal.log_write.write("Not adding" + str(url_list[0][1]) + "to list to download already in DB.")
                    
                else:
                
                    print("Will download:", str(self.parsed_data[each]["pic"]), '!')
                    universal.log_write.write("Adding file: " + str(self.parsed_data[each]["pic"]) + " to DB.")
                    
            # Using Cleaned keys from DB
            for each in self.cleaned_data.keys():
                self._pics[self.cleaned_data[each]["id"]] = self.cleaned_data[each]["pic"]
                self._filename[self.cleaned_data[each]["id"]] = self.cleaned_data[each]["filename"]

            # Returns Cleaned data(urls, tags and whatever the parser wants)
            # Returns A list of files downloaded from downloader
            return self.download_pic(), self.cleaned_data

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
        
        self.formattedData = {}
        
        # TODO NEED to make a way to stop this from downloading to prevent an ugly error message.

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
    
                    universal.log_write.write("Downloaded file: " + str(filepath) + " !")

                individualData.append(self._filename[each])
                individualData.append(image_hash)
            
            self.formattedData[each] = individualData
        return self.formattedData
