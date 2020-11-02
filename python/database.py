'''
database.py Interacts With Sqlite3 Database.
'''

import sqlite3

class Database():
    '''
    Interaction Handler between database and everything else
    '''
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

    def create_default(self):
        '''
        Creates Default Database
        '''
        self.cursor.execute('''CREATE TABLE File(hash text, size real, ext text, tags text)''')
        self.cursor.execute('''CREATE TABLE Tags(id real, name text, parents text)''')
        self.cursor.execute('''CREATE TABLE Parents(id real, name text, children text)''')
        self.cursor.execute('''CREATE TABLE Settings(name text, pretty text, \
        num real, param text)''')
