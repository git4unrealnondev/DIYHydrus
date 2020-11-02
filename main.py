"""
Main.py Initial sanity checker and bootup
"""


import os
import argparse
import sys

import python.logger as logger
import python.database as database
import python.qt5 as qt

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

        self.database = database.Database(db_dir)
        if not self.sanity_check(db_dir):
            self.create_database()

        self.QTHANDLE = qt.qt5()

    def sanity_check(self, db_dir):
        '''
        Checks DB Location & Exits if is a file.
        Establishes a log file aswell.
        Returns True if DB exists.
        Returns False if DB does not exist.
        '''

        if os.path.exists(db_dir) and os.path.isfile(db_dir):
            if self.verbose:
                print("ERROR DB IS FILE?")
            self.log_write = logger.LoggerHandler(db_dir)
            self.log_write.write("INCORRECT DB LOCATION, IS A FILE???")
            sys.exit()
            return False
        if os.path.exists(db_dir + "main.db"):
            self.log_write = logger.LoggerHandler(db_dir)
            if self.verbose:
                print("DB ALREADY EXISTS")
            self.log_write.write("DB EXISTS.")
            return True
        else:
            self.log_write = logger.LoggerHandler(db_dir)
            if self.verbose:
                print("DB DOES NOT EXIST")
            self.log_write.write("DB Does not exist Creating at Default Dir.")
            return False
    def create_database(self):
        '''
        Creates Database from structure found in python/database.py
        Auto writes on complete
        '''
        self.database.create_default()

CheckBoot()
