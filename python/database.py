'''
database.py Interacts With Sqlite3 Database.
'''

import sqlite3

class Database():

    def __init__(self, directory):
        self.conn = sqlite3.connect(str(directory) + 'main.db')
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()
        
    def write(self):
        self.conn.commit()

    def create_default(self):
        self.c.execute('''CREATE TABLE File(hash text, size real, ext text, tags text)''')
        self.c.execute('''CREATE TABLE Tags(id real, name text, parents text)''')
        self.c.execute('''CREATE TABLE Parents(id real, name text, children text)''')
