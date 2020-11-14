'''
database.py Interacts With Sqlite3 Database.
'''

import sqlite3
import sys

import python.globals as globals

class Database():
    '''
    Interaction Handler between database and everything else
    '''
    VERSION = 1

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

    def db_update(self):
        print ("Tring to update DB (NOT IMPLEMENTED POGGERS :D)")
        globals.log_write.write("Update test")
    def db_sanity(self):
        '''
        Checks Database sanity and ensures that Database is the same version as the others.
        '''
        result = self.cursor.execute("SELECT * from Settings WHERE name = 'VERSION'").fetchone()
        if int(result[2]) < self.VERSION:
            self.db_update()
        elif int(result[2]) == self.VERSION:
            globals.log_write.write("Up To Date")
            print("Up To Date")
        else:
            globals.log_write.write("DB is More Advanced along then Program.")
            print("DB is More Advanced along then Program.")
            print("Exiting")
            sys.exit()

    def create_default(self):
        '''
        Creates Default Database
        '''
        self.cursor.execute('''CREATE TABLE File(hash text, size real, ext text, tags text)''')
        self.cursor.execute('''CREATE TABLE Tags(id real, name text, parents text)''')
        self.cursor.execute('''CREATE TABLE Parents(id real, name text, children text)''')
        self.cursor.execute('''CREATE TABLE Settings(name text, pretty text, num real, param text)''')
        
        # Adding Current Version into DB as First Thing Done
        self.cursor.execute("INSERT INTO Settings(name, pretty, num, param) VALUES(?, ?, ?, ?)", ("VERSION", None, self.VERSION, None))

        self.write()
        return

    def pull_scrapers(self):
        result = self.cursor.execute("SELECT * from Settings WHERE name = 'Scraper'").fetchall()
        print(result)
