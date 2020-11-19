'''
database.py Interacts With Sqlite3 Database.
'''

import sqlite3
import sys

import python.globals as universal

class Database():
    '''
    Interaction Handler between database and everything else
    '''
    VERSION = 2

    def __init__(self, directory):
        '''
        Creates Connector and Cursor for Database Interaction
        '''
        self.conn = sqlite3.connect(str(directory) + 'main.db')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def write(self):
        '''
        Commits changes to db & disk
        '''

        self.conn.commit()

    def db_update(self, dv, pv):
        print ("Tring to update DB (NOT IMPLEMENTED POGGERS :D)")
        universal.log_write.write("Update test")
        print(dv,pv)
        if int(dv) == 1 and int(pv) == 2:
            # Added in Version 1.1 for parser support
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Parsers(name text, url text, parser text)''')
            print("Upgrading from ", dv, " to ", pv)
            universal.log_write.write("Upgrading from V" + str(dv) + " to V" + str(pv))
            
        self.cursor.execute("UPDATE Settings set num = ? WHERE name = ?", (int(self.VERSION), "VERSION"))
        self.write()
    def db_sanity(self):
        '''
        Checks Database sanity and ensures that Database is the same version as the others.
        '''
        result = self.cursor.execute("SELECT * from Settings WHERE name = 'VERSION'").fetchone()
        if int(result[2]) < self.VERSION:
            self.db_update(result[2], self.VERSION)
        elif int(result[2]) == self.VERSION:
            universal.log_write.write("Up To Date")
            print("Up To Date")
        else:
            universal.log_write.write("DB is More Advanced along then Program.")
            print("DB is More Advanced along then Program.")
            print("Exiting")
            sys.exit()

    def create_default(self):
        '''
        Creates Default Database
        '''
        self.cursor.execute('''CREATE TABLE File(hash text, size real, ext text, tags text)''')
        self.cursor.execute('''CREATE TABLE Tags(id INTEGER, name text, parents text)''')
        self.cursor.execute('''CREATE TABLE Parents(id INTEGER, name text, children text)''')
        self.cursor.execute('''CREATE TABLE Settings(name text, pretty text, num INTEGER, param text)''')

        # Added in Version 1.1 for parser support
        self.cursor.execute('''CREATE TABLE Parsers(name text, url text, parser text)''')

        # Adding Current Version into DB as First Thing Done
        self.cursor.execute("INSERT INTO Settings(name, pretty, num, param) VALUES(?, ?, ?, ?)", ("VERSION", None, self.VERSION, None))

        self.write()
        return

    def pull_scrapers(self):
        ''' Returns a list of scrapers '''
        result = self.cursor.execute("SELECT * from Settings WHERE name = 'Scraper'").fetchall()
        return result
