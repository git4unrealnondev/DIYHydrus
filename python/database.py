'''
database.py Interacts With Sqlite3 Database.
'''

import sqlite3
import sys
import os

import urllib.parse

import python.globals as universal

class Database():
    '''
    Interaction Handler between database and everything else
    '''
    VERSION = 1
    
    hashestoignore = []

    def __init__(self, directory):
        '''
        Creates Connector and Cursor for Database Interaction
        '''
        self.conn = sqlite3.connect(str(directory) + 'main.db')
        self.cursor = self.conn.cursor()
        
        #self.pull_table("Namespace")
        
        #print("namespaces", self.namespaces)

    def __del__(self):
        self.conn.close()

    def write(self):
        '''
        Commits changes to db & disk
        '''

        self.conn.commit()

    def pull_table(self, table):
        pass
        #rows = self.cursor.execute("SELECT * FROM " + str(table)).fetchall()
        #for each in rows:
        #    print (each)
        #return 

    def db_update(self, dv, pv):
        print ("Tring to update DB (NOT IMPLEMENTED POGGERS :D)")
        universal.log_write.write("Update test")
        print(dv,pv)
        # Example DB Update Script
        #if int(dv) == 1 and int(pv) == 2:
        #    # Added in Version 1.1 for parser support
        #    self.cursor.execute('''CREATE TABLE IF NOT EXISTS Parsers(name text, url text, parser text)''')
        #    print("Upgrading from ", dv, " to ", pv)
        #    universal.log_write.write("Upgrading from V" + str(dv) + " to V" + str(pv))
        
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
            
        # Checking if Files Dir exists if not creates it.
        location = self.pull_data("Settings", "name", "FilesLoc")[0][3]
        if not os.path.exists(universal.db_dir + location):
            universal.log_write.write("Could not find File Storage Location Creating.")
            os.mkdir(universal.db_dir + location)
            
    def namespace_manager(self, key):
        '''
        Handles the namespace data insertion into the DB
        ONLY ADDS NEW x IF NOT PRESENT IN NAMESPACE.
        '''
        #print(key, self.cursor.execute("SELECT * from Namespace WHERE name = '" + key + "'").fetchall()[0])
        if not len(self.cursor.execute("SELECT * from Namespace WHERE name = '" + str(urllib.parse.quote(str(key))) + "'").fetchall()) >= 1:
        #if not key in self.cursor.execute("SELECT * from Namespace WHERE name = '" + key + "'").fetchall()[0]:
            datacpy = self.cursor.execute("SELECT count() from Namespace")
            value = datacpy.fetchone()[0] + 1
            self.cursor.execute("INSERT INTO Namespace(id, name, description) VALUES(?, ?, ?)", (value, str(urllib.parse.quote(str(key))), ""))
            
    def tag_namespace_manager(self, key, namespace):
        '''
        Same as namespace_manager but with slightly more advanced logic.
        ONLY ADDS NEW x IF NOT PRESENT IN TAGS.
        '''
       # print(key)
        if not len(self.cursor.execute("SELECT * from Tags WHERE name = '" + str(urllib.parse.quote(str(key))) + "'").fetchall()) >= 1:
            datacpy = self.cursor.execute("SELECT count() from Tags")
            value = datacpy.fetchone()[0] + 1
            
            # TODO add proper parents support
            
            namespace_id = self.pull_data("Namespace", "name", namespace)[0][0]
            #print("ID", namespace_id, namespace)
            #print("key", key)
            self.cursor.execute("INSERT INTO Tags(id, name,namespace) VALUES(?, ?, ?)", (value, str(urllib.parse.quote(str(key))), namespace_id))

    def file_manager(self, hash, filename, size, ext):
        #print(hash, filename,size,ext)
        if not len(self.cursor.execute("SELECT * from File WHERE hash = '" + str(hash) + "'").fetchall()) >= 1:
        #if not key in self.cursor.execute("SELECT * from Namespace WHERE name = '" + key + "'").fetchall()[0]:
            datacpy = self.cursor.execute("SELECT count() from File")
            value = datacpy.fetchone()[0] + 1
            self.cursor.execute("INSERT INTO File(id, hash, filename, size, ext) VALUES(?, ?, ?, ?, ?)", (value, hash, filename, size, ext))
        else:
            #print("File Manager ignoring hash: ", hash)
            self.hashestoignore.append(hash)
            #universal.log_write.write("File Manager ignoring hash: " + str(hash))

    def t_and_f_relation_manager(self, hash, tag):
        tagid  = self.cursor.execute("SELECT * from Tags WHERE name = '" + str(str(urllib.parse.quote(str(tag)))) + "'").fetchall()
        fileid = self.cursor.execute("SELECT * from File WHERE hash = '" + str(hash) + "'").fetchall()
        #print ("hash&tag ", hash, fileid[0][0], tag, tagid[0][0])
        #print(fileid, tagid)
        #print(tagid[0], fileid[0])
        
        if len(tagid) == 1 and len(fileid) == 1:
            if not hash in self.hashestoignore:
                self.cursor.execute("INSERT INTO RelationShip(fileid, tagid) VALUES(?, ?)", (fileid[0][0], tagid[0][0]))
            
        else:
            print("t and f error", tagid, fileid)

    def search_tags(self, tags):
        return self.pull_data("Tags", "name", str(str(urllib.parse.quote(str(tags)))))

    def search_relationships(self, tagid):
        return self.pull_data("RelationShip", "tagid", tagid)
        
    def pull_file(self, fileid):
        return self.pull_data("File", "id", fileid)
        
    def create_default(self):
        '''
        Creates Default Database
        '''
        self.cursor.execute('''CREATE TABLE File(id INTEGER, hash text, filename text,size real, ext text)''')
        self.cursor.execute('''CREATE TABLE Tags(id INTEGER, name text, parents INTEGER, namespace INTEGER)''')
        self.cursor.execute('''CREATE TABLE RelationShip(fileid INTEGER, tagid INTEGER)''')
        self.cursor.execute('''CREATE TABLE Parents(id INTEGER, name text, children text, namespace INTEGER)''')
        self.cursor.execute('''CREATE TABLE Namespace(id INTEGER, name text, description text)''')

        self.cursor.execute('''CREATE TABLE Settings(name text, pretty text, num INTEGER, param text)''')

        # Added in Version 1.1 for parser support
        self.cursor.execute('''CREATE TABLE Parsers(name text, url text, parser text)''')

        # Adding Current Version into DB as First Thing Done
        self.cursor.execute("INSERT INTO Settings(name, pretty, num, param) VALUES(?, ?, ?, ?)", ("VERSION", None, self.VERSION, None))
        self.cursor.execute("INSERT INTO Settings(name, pretty, num, param) VALUES(?, ?, ?, ?)", ("DEFAULTRATELIMIT", None, 5, None))
        self.cursor.execute("INSERT INTO Settings(name, pretty, num, param) VALUES(?, ?, ?, ?)", ("FilesLoc", None, None, "Files/"))
        self.cursor.execute("INSERT INTO Settings(name, pretty, num, param) VALUES(?, ?, ?, ?)", ("DEFAULTUSERAGENT", None, None, "DIYHydrus/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 DIYHydrus/10.0"))
        self.write()
        return

    # TODO Cache returns to here in memory for further optimizations.
    def pull_data(self, table, collumn, search_term):
        return self.cursor.execute("SELECT * from " + str(table) + " WHERE " + str(collumn) + " = '" + str(search_term) + "'").fetchall()

    def pull_scrapers(self):
        ''' Returns a list of scrapers '''
        result = self.cursor.execute("SELECT * from Settings WHERE name = 'Scraper'").fetchall()
        return result
