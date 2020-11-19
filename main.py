"""
Main.py Initial sanity checker and bootup
"""

import os
import argparse
import sys
import python.globals as universal

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
        parser.add_argument('-s', "--AddScraper", type=str, help='Adds a scraper to Database')
        parser.add_argument('-v', "--verbose", type=str, help='Enables Verbose Logging' + \
            'NOT YET IMPLEMENTED')
        args = parser.parse_args()

        if args.verbose is None:
            self.verbose = False
        else:
            self.verbose = True

        if args.dbDir is None:
            db_dir = "db/"
        else:
            db_dir = args.dbDir

        self.sanity_check(db_dir)

        # Creates Scraper Handler for db Scraping
        universal.scraperHandler = universal.scraper.ScraperClass()

        # Overrides scraper creation if scraper option is selected
        if not args.AddScraper is None:
            universal.scraperHandler.replace_scraper(args.AddScraper)
        else:
            # Scrapes URL Using scraper Handler.
            if not args.url is None:
                universal.scraperHandler.scrape(args.url)

       # DB Has Passed Handler Will Init GUI Now
       # self.QTHANDLE = qt.qt5()

    def sanity_check(self, db_dir):
        '''
        Checks DB Location & Exits if is a file.
        Establishes a log file aswell.
        Returns True if DB exists.
        Returns False if DB does not exist.
        '''

        if not os.path.exists(db_dir):
            print("DB DIR does not exist :C ", db_dir)
            sys.exit()

        if os.path.exists(db_dir) and os.path.isfile(db_dir):
            if self.verbose:
                print("ERROR DB IS FILE?")
            universal.log_write = universal.logger.LoggerHandler(db_dir)
            self.log_write.write("INCORRECT DB LOCATION, IS A FILE???")
            sys.exit()

        if os.path.exists(db_dir + "main.db"):
            universal.log_write = universal.logger.LoggerHandler(db_dir)
            if self.verbose:
                print("DB ALREADY EXISTS")
            universal.log_write.write("DB EXISTS.")
            universal.databaseRef = universal.database.Database(db_dir)
            universal.databaseRef.db_sanity()
        else:
            universal.log_write = universal.logger.LoggerHandler(db_dir)
            if self.verbose:
                print("DB DOES NOT EXIST")
            universal.log_write.write("DB Does not exist Creating at Default Dir.")
            universal.databaseRef = universal.database.Database(db_dir)
            universal.databaseRef.create_default()
            universal.databaseRef.db_sanity()

    def create_database(self):
        '''
        Creates Database from structure found in python/database.py
        Auto writes on complete
        '''
        self.database.create_default()

CheckBoot()
