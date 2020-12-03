"""
Main.py Initial sanity checker and bootup
"""

import os
import argparse
import sys
import python.global_vars as universal

# Gets Called as python gets invoked.
class CheckBoot():
    '''
    A class object to neaten code.
    Parses flags from terminal.
    Initalizes DB
    '''
    def __init__(self):
        parser = argparse.ArgumentParser(description='Custom Databasing Program')
        parser.add_argument('-d', "--dbDir", type=str, help='Alternative DB Location')
        parser.add_argument('-u', "--url", type=str, help='url for test scraping')
        parser.add_argument('-a', "--AddScraper", type=str, help='Adds a scraper to Database')
        parser.add_argument('-s', "--Search", type=str, help='Searches DB use quotes when spacing')
        parser.add_argument('-v', "--verbose", type=str, help='Enables Verbose Logging' + \
            'NOT YET IMPLEMENTED')
        parser.add_argument('-ps', action="store_true",help='Searches query with parser')
        args = parser.parse_args()

        if args.verbose is None:
            self.verbose = False
        else:
            self.verbose = True

        if args.dbDir is None:
            db_dir = "db/"
        else:
            db_dir = args.dbDir

        # Used by fileDownloader
        universal.db_dir = db_dir

        self.sanity_check(db_dir)

        universal.pluginManager = universal.plugin.PluginHandler(universal)

        # Creates Scraper Handler for Scraping
        universal.scraperHandler = universal.scraper.ScraperClass(universal)

        # Overrides scraper creation if scraper option is selected
        if not args.AddScraper is None:
            print("b")
            universal.scraperHandler.replace_scraper(args.AddScraper, args.url)



        # Scrapes URL Using scraper Handler.
        if not args.url is None and not args.ps:
            print("a")
            universal.scraperHandler.scrape(args.url)
        elif args.url is None and args.ps:
            print("c")
            universal.scraperHandler.scrape(args.ps, args.AddScraper, args.Search)
        if not args.Search is None:
            universal.commons.search_handler(args.Search)

    def __del__(self):

        if not universal.scraperHandler is None:
            del universal.scraperHandler

        if not universal.pluginManager is None:
            del universal.pluginManager
            
        if not universal.databaseRef is None:
            del universal.databaseRef

    def sanity_check(self, db_dir):
        '''
        Checks DB Location & Exits if is a file.
        Establishes a log file aswell.
        Returns True if DB exists.
        Returns False if DB does not exist.
        '''

        if not os.path.exists(db_dir):
            print("DB DIR does not exist :C ", db_dir)
            os.mkdir(db_dir)

        if os.path.exists(db_dir) and os.path.isfile(db_dir):
            if self.verbose:
                print("ERROR DB IS FILE?")
            universal.log_write = universal.logger.LoggerHandler(db_dir)
            universal.log_write.write("INCORRECT DB LOCATION, IS A FILE???")
            sys.exit()

        if os.path.exists(db_dir + "main.db"):
            universal.log_write = universal.logger.LoggerHandler(db_dir)
            if self.verbose:
                print("DB ALREADY EXISTS")
            universal.log_write.write("DB EXISTS.")
            universal.databaseRef = universal.database.Database(db_dir, universal)
            universal.databaseRef.db_sanity()
        else:
            universal.log_write = universal.logger.LoggerHandler(db_dir)
            if self.verbose:
                print("DB DOES NOT EXIST")
            universal.log_write.write("DB Does not exist Creating at Default Dir.")
            universal.databaseRef = universal.database.Database(db_dir, universal)
            universal.databaseRef.create_default()
            universal.databaseRef.db_sanity()

    def create_database(self):
        '''
        Creates Database from structure found in python/database.py
        Auto writes on complete
        '''
        universal.databaseRef.create_default()

CheckBoot()
