"""
Handler For Loading and Deploying Scrapers
"""
import python.global_vars as universal
import os

class ScraperClass():
    '''
    Loads, runs scrapers
    '''
    scraper_rate_limited = None

    def __init__(self, universal):
        """
        Loads and Initlizes the scrapers into Memory.
        """

        self.universal = universal

        self.scraper_folder_managment()

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
            #for each in self.universal.scraper_store:
            #    each.removal()

    def scraper_folder_managment(self):
        '''
        manages the loading and scraping of webpages.
        '''
        SCRAPER_DIR = "scrapers/"
        if not os.path.exists(SCRAPER_DIR):
            os.mkdir(SCRAPER_DIR)

        temp_list = []
        #for files in os.listdir(SCRAPER_DIR):
        #    self.replace_scraper(SCRAPER_DIR + files)


    def scrape(self, url, *args):
        '''
        Checks to see if scraper exists and if it doesn't it will prompt the user to create one.
        '''

        #A Search command Has been issued
        if isinstance(url, bool) and not args[0] is None:
            print("User has overridden url splitting or none was applied!!!")
            # Pulling ratelimited INSTANCE TO BE USED

            scraper_name = args[0].split('/')[1].split('.')[0]
            search = args[1]
            self.scraper_rate_limited = self.universal.scraper_list[scraper_name]
            #print(self.universal.scraper_list, scraper_name, search)
            self.scraper_rate_limited.search_term = search
            downloaded_files, parsed_data = self.scraper_rate_limited.request_data()
            self.interpret_data(parsed_data, downloaded_files)
            #self.scraper_rate_limited = self.universal.scraper_list[url.split('/')[2]]

            # SCRAPER handles the DB calls, sorts things out.
            #downloaded_files, parsed_data = self.scraper_rate_limited.request_data()
            #self.interpret_data(parsed_data, downloaded_files)

        #Might not be needed
        #elif url.split('/')[2] in self.universal.scraper_list.keys():





        #Normal URL has been passed
        if isinstance(url, str):
            print(self.universal.scraper_list)
            print("Found Scraper", url.split('/')[2].split('.')[0])
            self.universal.log_write.write("Found Scraper " + url.split('/')[2].split('.')[0] + " ScrapersDB")
            # Pulling ratelimited INSTANCE TO BE USED
            self.scraper_rate_limited = self.universal.scraper_list[url.split('/')[2].split('.')[0]]
            # SCRAPER handles the DB calls, sorts things out.
            downloaded_files, parsed_data = self.scraper_rate_limited.request_data()
            self.interpret_data(parsed_data, downloaded_files)

    def interpret_data(self, data, file_data):
        '''
        Parses data from parser into fields the DB can understand.
        Adds changes to DB and writes on finish.
        '''
        tags_in_db = self.universal.databaseRef.pull_data("Tags", "name", None)
        for each in data.keys():
            for every in data[each]:
                if every in tags_in_db:
                    data[each].pop(every)
        for each in data.keys():

            if each in file_data.keys():

                self.universal.databaseRef.file_manager(\
                    file_data[each][1], file_data[each][0], None, file_data[each][0].split('.')[1])

            for every in data[each]:

                self.universal.databaseRef.namespace_manager(every)

                if isinstance(data[each][every], list):

                    for tag in data[each][every]:

                        self.universal.databaseRef.tag_namespace_manager(tag, every)

                        self.universal.databaseRef.t_and_f_relation_manager(file_data[each][1], tag)

                elif isinstance(data[each][every], dict):
                    for tag in data[each][every].keys():

                        self.universal.databaseRef.tag_namespace_manager(tag, every)

                        self.universal.databaseRef.t_and_f_relation_manager(file_data[each][1], tag)

                elif isinstance(data[each][every], str):

                    self.universal.databaseRef.tag_namespace_manager(data[each][every], every)

                    self.universal.databaseRef.t_and_f_relation_manager(\
                            file_data[each][1], data[each][every])

                elif isinstance(data[each][every], int):

                    self.universal.databaseRef.tag_namespace_manager(data[each][every], every)

                    self.universal.databaseRef.t_and_f_relation_manager(\
                        file_data[each][1], data[each][every])

            self.universal.pluginManager.callback("database_writing", data[each], file_data[each][1], file_data[each][0])
        self.universal.databaseRef.write()




    def scraper_list_handler(self, scraper_name, pulled_data, url):
        '''
        Handles scraper objects for rate limiting.
        Adds pulled data into scraper from script pulled data.
        '''
        if "USER_AGENT" in pulled_data.keys():
            user_agent = pulled_data["USER_AGENT"]
        else:
            print("COULD NOT FIND USER_AGENT IN", scraper_name, "!", " DEFAULTING TO DB DEFAULT!")
            self.universal.log_write.write("COULD NOT FIND USER_AGENT IN " + \
                scraper_name + "!" + " DEFAULTING TO DB DEFAULT.")
            user_agent = self.universal.databaseRef.pull_data(
                "Settings",
                "name",
                "DEFAULTUSERAGENT")[0][3]
        if "RATE_LIMIT" in pulled_data.keys():
            rate_limit = pulled_data["RATE_LIMIT"]
        else:
            print("COULD NOT FIND RATE_LIMIT IN", scraper_name, "!", " DEFAULTING TO DB DEFAULT!")
            self.universal.log_write.write("COULD NOT FIND RATE_LIMIT IN " + \
                                      scraper_name + "!" + " DEFAULTING TO DB DEFAULT.")
            rate_limit = self.universal.databaseRef.pull_data(
                "Settings",
                "name",
                "DEFAULTRATELIMIT")[0][2]
        #print("Parsed Data", "USERAGENT:", user_agent, "RATELIMIT:", rate_limit)

        if not scraper_name in self.universal.scraper_list:
            #if "SELF_HANDLE_CONNECTION" in pulled_data.keys():
            self.universal.scraper_list[scraper_name] = self.universal.rateLimiter.InternetHandler(
                    user_agent, rate_limit, url, self.universal, scraper_name, True)
            #else:
            # Scraper is not in list need to create a new one and append to scraper list.
            #    self.universal.scraper_list[scraper_name] = self.universal.rateLimiter.InternetHandler(
            #        user_agent, rate_limit, url, self.universal)
        return self.universal.scraper_list[scraper_name]

    def run_scraper(self, filename, script, *args):
        '''
        Runs Scraper from memory
        Reads variables from script into new fileDownloader instance &
        Adds new fileDownloader into self.universal.scraper_list w/
        the name being the websites URL and the fileDownloader as its value.

        args[0] is the script thats loaded into memory
        args[1] is the URL thats will be scraped
        args[2] is the web_data pulled from fileDownloader
        '''

        print("filename", filename)
        for each in args:
            print("args", args.index(each),each)

        url = None

        if not args[0] is None:
            url = args[0]

        # Initing a passthrough Variable
        # loc contains ALL VARIABLES & FUNCTION CALLS IN SCRIPT
        loc = {}
        #Called to Init vars
        if isinstance(args[0], str) or args[0] is None:
            print("type", type(args[0]))
            exec(script, {"universal": self.universal}, loc)

        elif args[0] is None:
            print("args[0]")
            pass
        # Runs Scraper
        else:
            print("args", args[0], type(args[0]))
            exec(script, {"universal": self.universal, "web_data": args[0]}, loc)
            return loc["stored_data"]
        # Reading scraper into universal memory
        if len(filename.split('/')) > 1 and not url is None and not isinstance(args[0], list):

            self.scraper_list_handler(filename.split('/')[1].split('.')[0], loc, url)

        else:
            self.scraper_list_handler(filename.split('/')[1].split('.')[0], loc, None)

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
                self.universal.scraper_store[scraper_file.split('/')[1].split('.')[0]] = script_string
            except AttributeError:
                print("I see that you have not specified URL's")

        elif len(args) == 0:
            print("I am not running scraper " + scraper_file + " .")
            self.universal.log_write.write("I am not running scraper " + scraper_file + " .")
            return
        #Executes Script
        self.run_scraper(scraper_file, script_string, args[0])
