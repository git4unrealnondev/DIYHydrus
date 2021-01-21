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
    _tag_data = {}
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

        data = self.parsed_data
        temp = {}

        if self.formatted_data is None:
            return None, None
        #Changed
        for each in self.formatted_data:
            temp[each] = data[each]

        return self.formatted_data, temp

    @staticmethod
    def limit(until, *args):
        '''
        Shows rate limited dialagoue when getting rate limited.
        '''
        print("Rate Limited")

    def request_data(self):
        '''
        Pulls data from website and gets a list of pictures to download.
        '''
        self.parsed_data = self.universal.scraperHandler.run_scraper(self.filename, self.universal.scraper_store[self.filename], [self._spider[-1], self.rate_limiter, self])

        # Function cleans files based on picture source already being inside the DB.
        try:
            tempstore = self.parsed_data.copy()
        except AttributeError:
            print("ERROR PARSER:", str( \
                                self._spider[-1].split('/')[2]), "DID NOT RETURN ANY DATA TO BE PARSED.")
            self.universal.log_write.write("ERROR PARSER:" + str( \
                                self._spider[-1].split('/')[2]) + " DID NOT RETURN ANY DATA TO BE PARSED.")
            raise AttributeError("Stopping program")

        tag_to_download = {}

        #Optimized code for large DB searches

        tag_data = self.universal.databaseRef.pull_data("Tags", "name", None)
        tag_parsed = [a[:2][1] for a in tag_data]

        #Pulls tagid's from DB
        for each in tag_parsed:
            if each.isdigit():
                if int(each) in tempstore:
                    tempstore.pop(int(each))

        for each in tempstore:
            self._pics[tempstore[each]["id"]] = tempstore[each]["pic"]
            self._filename[tempstore[each]["id"]] = tempstore[each]["filename"]
            self._tag_data[tempstore[each]["id"]] = tempstore[each]
        print("I have to download:", len(tempstore), "Files.")

        self.download_pic()

    @staticmethod
    def hash256(image_ref):
        '''
        Hashes file with sha256.
        '''
        file_hash = hashlib.sha256()

        for data in image_ref.iter_content(8192):
            file_hash.update(data)

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

        return self.universal.db_dir + databaseloc + hone + htwo

    def normal_requests(self, url):
        with self.rate_limiter:
            page = requests.get(url, headers={'User-Agent': self.user_agent})
            return page
    def download_tags(self):
        print("tags")

    def download_pic(self):
        '''
        Downloads pictures to storage.
        @return List of files that has been downloaded (used for shutdown)
        '''
        self.formatted_data = {}
        print("Download Pic")
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

                    print("Downloaded file", self._filename[each])
                    self.universal.log_write.write("Downloaded file: " + str(filepath) + str(self._filename[each])+ " !")

                ##Processing data to avoid processing on close.
                #temp_dict = {}
                #temp_dict[each] = individual_data
                #self.parent.interpret_data(temp_dict, self.parsed_data[each])

                #Callback for plugin system
                self.universal.pluginManager.callback("file_download", filepath, self._filename[each], image_hash, self._tag_data[each])

                #Test to enable live processing of data
                self.universal.scraperHandler.interpret_data({"Empty": self._tag_data[each]}, {"Empty": [ self._filename[each], image_hash]})

                #print(self.universal.databaseRef.memorydb)

                individual_data.append(self._filename[each])
                individual_data.append(image_hash)

            self.formatted_data[each] = individual_data
        return self.formatted_data
