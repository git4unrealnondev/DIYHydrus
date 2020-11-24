"""
Handler For Loading and Deploying Scrapers
"""
import python.global_vars as universal

class ScraperClass():
    '''
    Loads, runs scrapers
    '''
    scraper_rate_limited = None

    def __init__(self):
        """
        Loads and Initlizes the scrapers into Memory.
        """
        #for each in universal.databaseRef.pull_scrapers():
        #    print(each)
        #    self.scraper_list_handler(each)

        # Adding a scraper list for rate limiting
        universal.scraper_list = {}
        universal.scraper_store = {}

    def __del__(self):
        if not self.scraper_rate_limited is None:
            downloaded_files, parsed_data = self.scraper_rate_limited.removal()

            if downloaded_files is None and parsed_data is None:
                return
            # Interprets and prepares data for database.
            self.interpret_data(parsed_data, downloaded_files)
            #for each in universal.scraper_store:
            #    each.removal()

    def scrape(self, url):
        '''
        Checks to see if scraper exists and if it doesn't it will prompt the user to create one.
        '''
        if url.split('/')[2] in universal.scraper_list.keys():
            print("Found Scraper", url.split('/')[2])
            #print("keys", universal.scraper_list.keys(), URL.split('/')[2])
            universal.log_write.write("Found Scraper " + url.split('/')[2] + " ScrapersDB")

            # Pulling ratelimited INSTANCE TO BE USED
            self.scraper_rate_limited = universal.scraper_list[url.split('/')[2]]

            # DONE Potential INSERTION point for files already in DB
            # SCRAPER handles the DB calls, sorts things out.
            downloaded_files, parsed_data = self.scraper_rate_limited.request_data()

            # downloadedFiles contains filename & sha256 hash
            #for each in downloadedFiles:
            #    print(each)

            #for each in parsed_data.keys():
            #    print(parsed_data[each])

            # Interprets and prepares data for database.
            self.interpret_data(parsed_data, downloaded_files)

    @staticmethod
    def interpret_data(data, file_data):
        '''
        Parses data from parser into fields the DB can understand.
        Adds changes to DB and writes on finish.
        '''
        for each in data.keys():

            universal.databaseRef.file_manager(\
                file_data[each][1], file_data[each][0], None, file_data[each][0].split('.')[1])

            for every in data[each]:

                universal.databaseRef.namespace_manager(every)

                if isinstance(data[each][every], list):
                    for tag in data[each][every]:
                        #print("List", ec)
                        #print('1')
                        universal.databaseRef.tag_namespace_manager(tag, every)

                        universal.databaseRef.t_and_f_relation_manager(file_data[each][1], tag)

                if isinstance(data[each][every], dict):
                    for tag in data[each][every].keys():
                        #print('2')
                        universal.databaseRef.tag_namespace_manager(tag, every)

                        universal.databaseRef.t_and_f_relation_manager(file_data[each][1], tag)

                        #print("Dict", ec, data[each][every][ec])
                if isinstance(data[each][every], str):
                    #print(data[each][every])
                    #print("every", every, data[each][every])
                    #print('3')
                    universal.databaseRef.tag_namespace_manager(data[each][every], every)

                    universal.databaseRef.t_and_f_relation_manager(\
                            file_data[each][1], data[each][every])

                if isinstance(data[each][every], int):

                    #print("every", every, data[each][every])
                    universal.databaseRef.tag_namespace_manager(data[each][every], every)
                    #print('4')
                    #print(every, data[each][every])
                    universal.databaseRef.t_and_f_relation_manager(\
                        file_data[each][1], data[each][every])

                #print(every ,data[each][every])

        universal.databaseRef.write()

    @staticmethod
    def scraper_list_handler(scraper_name, pulled_data, url):
        '''
        Handles scraper objects for rate limiting.
        Adds pulled data into scraper from script pulled data.
        '''
        if "USER_AGENT" in pulled_data.keys():
            user_agent = pulled_data["USER_AGENT"]
        else:
            print("COULD NOT FIND USER_AGENT IN", scraper_name, "!", " DEFAULTING TO DB DEFAULT!")
            universal.log_write.write("COULD NOT FIND USER_AGENT IN " + \
                scraper_name + "!" + " DEFAULTING TO DB DEFAULT.")
            user_agent = universal.databaseRef.pull_data(
                "Settings",
                "name",
                "DEFAULTUSERAGENT")[0][3]
        if "RATE_LIMIT" in pulled_data.keys():
            rate_limit = pulled_data["RATE_LIMIT"]
        else:
            print("COULD NOT FIND RATE_LIMIT IN", scraper_name, "!", " DEFAULTING TO DB DEFAULT!")
            universal.log_write.write("COULD NOT FIND RATE_LIMIT IN " + \
                                      scraper_name + "!" + " DEFAULTING TO DB DEFAULT.")
            rate_limit = universal.databaseRef.pull_data(
                "Settings",
                "name",
                "DEFAULTRATELIMIT")[0][2]
        print("Parsed Data", "USERAGENT:", user_agent, "RATELIMIT:", rate_limit)

        if not scraper_name in universal.scraper_list:

            # Scraper is not in list need to create a new one and append to scraper list.
            universal.scraper_list[scraper_name] = universal.rateLimiter.InternetHandler(
                user_agent, rate_limit, url)
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
            script_string = args[0]
            url = args[1]

        # URL HAS NOT been passed into scraper
        elif args[1] is None:
            script_string = args[0]
            print("I Need the URL for the scraper to work")
            url = input(": ")

        else:
            print("A Stupid Code error has happened in run_scraper.")
            universal.log_write.write("A Stupid Code error has happened in run_scraper.")
            universal.log_write.write("DEBUG AS FOLLOWS")
            universal.log_write.write(args)

        # Initing a passthrough Variable
        # loc contains ALL VARIABLES & FUNCTION CALLS IN SCRIPT
        loc = {}
        if len(args) == 3:
            exec(script_string, {"universal": universal, "web_data": args[2]}, loc)
	        #print(loc)
            return loc['stored_data']
        if len(args) != 3:
            exec(script_string, {"universal": universal}, loc)
            # Passes URL to scraper to add to universal.scraper_list
            self.scraper_list_handler(url.split('/')[2], loc, url)
            return None
        return None
    def replace_scraper(self, scraper_file, *args):
        '''
        Reads Scraper into Memory
        '''
        script_string = ""

        #Reads script into memory
        with open(scraper_file, "r") as infile:
            for each in infile:
                script_string += each + "\n"

        #Places Script into scraper_store
        if not script_string is None:
            try:
                universal.scraper_store[args[0].split('/')[2]] = script_string
            except AttributeError:
                print("I see that you have not specified URL's")

        #Executes Script
        self.run_scraper(script_string, args[0])
