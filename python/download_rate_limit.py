'''
Handles file downloading and parser variable loading.
'''
import os
import urllib
import hashlib
import requests

from ratelimiter import RateLimiter

#import python.global_vars as universal


class InternetHandler():
    '''
    Handles file downloading from scraper.
    '''
    _pics = {}
    _spider = []
    _filename = {}
    filename = None
    search_term = None
    _init_url = None
    parsed_data = None
    cleaned_data = None
    formatted_data = None
    _bypass_requests = False
    def __init__(self, user_agent, rate_limit, URL, universal, filename, *args):
        self.user_agent = user_agent
        self.rate_limit = rate_limit
        self._spider.append(URL)
        self._init_url = URL
        self.filename = filename
        if len(args) > 0:
            self._bypass_requests = args[0]

        self.rate_limiter = RateLimiter(max_calls=self.rate_limit, period=10, callback=self.limit)

        self.universal = universal

    def return_url(self):
        return _init_url

    def removal(self):
        '''
        Trims list to hand to scraper for database adding upon untimely close.
        '''
        #for each in self.formatted_data:
        #print("Parsed_DATA", self.parsed_data)

        #print("len", len(self.formatted_data), len(self.parsed_data))

        data = self.parsed_data
        temp = {}

        #print(self.formatted_data)

        #print(self.parsed_data)

        if self.formatted_data is None:
            return None, None
        #Changed
        for each in self.formatted_data:
            temp[each] = data[each]
        #print(len(data), len(data) - len(self.formatted_data), type(data))
        #print(len(temp))
        return self.formatted_data, temp

    @staticmethod
    def limit(until, *args):
        '''
        Shows rate limited dialagoue when getting rate limited.
        '''
        print("Rate Limited for ", until, *args)

    def request_data(self):
        '''
        Pulls data from website and gets a list of pictures to download.
        '''
        with self.rate_limiter:
            #This handles if the scraper needs to control the connections.
            #IE: Cloudflare websites and / or custom scraping needs.
            # Instead of pulled web data it passes a list with the URL and a rate limiter object.
            #if not self._bypass_requests:
            #    page = requests.get(self._spider[-1], headers={'User-Agent': self.user_agent})
            #    self.parsed_data = self.universal.scraperHandler.run_scraper(str(self.universal.scraper_store \
            #                        [self._spider[-1].split('/')[2]]), self._spider[-1], page)
#
#            else:
            self.parsed_data = self.universal.scraperHandler.run_scraper(self.filename, self.universal.scraper_store[self.filename], [self._spider[-1], self.rate_limiter, self])

            # Function cleans files based on picture source already being inside the DB.
            try:
                print("parsed", type(self.parsed_data))
                self.cleaned_data = self.parsed_data.copy()
            except AttributeError:
                print("ERROR PARSER:", str( \
                                    self._spider[-1].split('/')[2]), "DID NOT RETURN ANY DATA TO BE PARSED.")
                self.universal.log_write.write("ERROR PARSER:" + str( \
                                    self._spider[-1].split('/')[2]) + " DID NOT RETURN ANY DATA TO BE PARSED.")
                raise AttributeError("Stopping program")
                
            tag_to_download = {}
                
            for each in self.parsed_data.keys():
                #print(self.parsed_data[each]["pic"])
                url_list = self.universal.databaseRef.pull_data("Tags", "name", \
                            str(str(urllib.parse.quote(str(self.parsed_data[each]["pic"])))))
                #print(url_list)
                del_cleaned_data = False
                if not len(url_list) == 0:
                    if not url_list[0][1] == []:
                        del_cleaned_data = True
                        if not len(url_list) == 0:
                           print("Not adding", url_list[0][1], "to list to download already in DB.")
                           self.universal.log_write.write("Not adding" + str(url_list[0][1]) + \
                                              "to list to download already in DB.")
                        else:
                           print("adding error")
                    else:

                        print("Will download:", str(self.parsed_data[each]["pic"]), '!')
                        self.universal.log_write.write("Adding file: " + \
                                              str(self.parsed_data[each]["pic"]) + " to DB.")
                
                    if url_list[0][1] == urllib.parse.quote(str(self.parsed_data[each]["pic"])):
                        print("File is already in DB updating info. Not yeet implemented.")
                        tag_to_download[each] = self.cleaned_data[each]
                
                    if del_cleaned_data:
                        #print("del_data", self.cleaned_data[each], each)
                        
                        del self.cleaned_data[each]
                    #print(self.cleaned_data)
                    #print("tags", self.cleaned_data)

            # Using Cleaned keys from DB
            for each in self.cleaned_data.keys():
                self._pics[self.cleaned_data[each]["id"]] = self.cleaned_data[each]["pic"]
                self._filename[self.cleaned_data[each]["id"]] = self.cleaned_data[each]["filename"]
    
                #print("pics", self._pics)
    
                # Returns Cleaned data(urls, tags and whatever the parser wants)
             # Returns A list of files downloaded from downloader
            return self.download_pic(), self.cleaned_data

    @staticmethod
    def hash256(image_ref):
        '''
        Hashes file with sha256.
        '''
        file_hash = hashlib.sha256()
        for data in image_ref.iter_content(8192):
            file_hash.update(data)
        #file_hash.update(image_ref)
        print(file_hash.hexdigest())
        return file_hash.hexdigest()

    
    def check_dir(self, hash_input):
        '''
        Creates file storage location if not exist.
        @return the file download location
        '''
        hone = ''
        htwo = ''
        hone = str(hash_input)[0] + str(hash_input)[1] + '/'
        htwo = str(hash_input)[2] + str(hash_input)[3] + '/'

        databaseloc = self.universal.databaseRef.pull_data("Settings", "name", "FilesLoc")[0][3]

        if not os.path.isdir(self.universal.db_dir + databaseloc + hone):
            os.mkdir(self.universal.db_dir + databaseloc + hone)
        if not os.path.isdir(self.universal.db_dir + databaseloc + hone + htwo):
            os.mkdir(self.universal.db_dir + databaseloc + hone + htwo)
        #print(hone, htwo)

        return self.universal.db_dir + databaseloc + hone + htwo

    def normal_requests(self, url):
        with self.rate_limiter:
            page = requests.get(url, headers={'User-Agent': self.user_agent})
            return page
    def download_tags(self):
        print("tags")

    def download_pic(self):
        '''
        Downloads a picture to storage.
        @return List of files that has been downloaded (used for shutdown)
        '''
        self.formatted_data = {}

        # TODO NEED to make a way to stop this from downloading to prevent an ugly error message.

        # NEEDS TO BE IN THIS ORDER FOR RATE LIMITING TO WORK PROPERLY
        for each in self._pics:
            individual_data = []
            with self.rate_limiter:

                # Code shamelessly stolen from:
                # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
                with requests.get(self._pics[each]) as request_data:
                    request_data.raise_for_status()


                    #r.raise_for_status()
                    image_hash = self.hash256(request_data)
                    request_data.raw.decode_content = False

                    filepath = self.check_dir(image_hash)

                    with open(filepath + self._filename[each], 'wb') as file_temp:
                        for chunk in request_data.iter_content(chunk_size=8192):
                            file_temp.write(chunk)

                    self.universal.log_write.write("Downloaded file: " + str(filepath) + " !")

                #Callback for plugin system
                self.universal.pluginManager.callback("file_download", filepath, self._filename[each], image_hash)

                individual_data.append(self._filename[each])
                individual_data.append(image_hash)

            self.formatted_data[each] = individual_data
        return self.formatted_data
