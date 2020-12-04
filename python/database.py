'''
database.py Interacts With Sqlite3 Database.
'''

import sqlite3
import sys
import os

import urllib.parse

class Database():
    '''
    Interaction Handler between database and everything else
    '''
    VERSION = 1

    hashestoignore = []

    def __init__(self, directory, universal):
        '''
        Creates Connector and Cursor for Database Interaction
        '''
        #self.conn = sqlite3.connect(str(directory) + 'main.db', check_same_thread=False)
        self.conn = sqlite3.connect(str(directory) + 'main.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("VACUUM")
        #creating universe handler
        self.universal = universal

    def __del__(self):
        self.write()
        self.conn.close()

    def write(self):
        '''
        Commits changes to db & disk
        '''

        self.conn.commit()

    def db_update(self, database_version, program_version):
        '''
        Location to add database updating args.
        IE: What needs to be done to update a database to a new version
        '''
        print("Tring to update DB (NOT IMPLEMENTED POGGERS :D)")
        self.universal.log_write.write("Update test")
        print(database_version, program_version)

        self.cursor.execute("UPDATE Settings set num = ? WHERE name = ?",
                            (int(self.VERSION), "VERSION"))
        self.write()
    def db_sanity(self):
        '''
        Checks Database sanity and ensures that Database is the same version as the others.
        '''
        result = self.cursor.execute("SELECT * from Settings WHERE name = 'VERSION'").fetchone()
        if int(result[2]) < self.VERSION:
            self.db_update(result[2], self.VERSION)
        elif int(result[2]) == self.VERSION:
            self.universal.log_write.write("Up To Date")
            print("Up To Date")
        else:
            self.universal.log_write.write("DB is More Advanced along then Program.")
            print("DB is More Advanced along then Program.")
            print("Exiting")
            sys.exit()

        # Checking if Files Dir exists if not creates it.
        location = self.pull_data("Settings", "name", "FilesLoc")[0][3]
        if not os.path.exists(self.universal.db_dir + location):
            self.universal.log_write.write("Could not find File Storage Location Creating.")
            os.mkdir(self.universal.db_dir + location)

    def create_table(self, table_name, db_format):
        '''
        Creates a database table if it does not exist.
        '''
        format_string = "("
        for each in db_format:
            print(each)
            format_string += each + " " + db_format[each] + " , "
        format_string = format_string[:-2]
        format_string += ")"
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + str(table_name) + " " + str(format_string))
        self.write()

    def namespace_manager(self, key):
        '''
        Handles the namespace data insertion into the DB
        ONLY ADDS NEW x IF NOT PRESENT IN NAMESPACE.
        '''
        if not len(self.cursor.execute("SELECT * from Namespace WHERE name = '" + \
                                       str(urllib.parse.quote(str(key))) + "'").fetchall()) >= 1:
        #if not key in self.cursor.execute("SELECT * from Namespace WHERE name = '" + \
                                           #key + "'").fetchall()[0]:
            datacpy = self.cursor.execute("SELECT count() from Namespace")
            value = datacpy.fetchone()[0] + 1
            self.cursor.execute("INSERT INTO Namespace(id, name, description) VALUES(?, ?, ?)", \
                                (value, str(urllib.parse.quote(str(key))), ""))

    def tag_namespace_manager(self, key, namespace):
        '''
        Same as namespace_manager but with slightly more advanced logic.
        ONLY ADDS NEW x IF NOT PRESENT IN TAGS.
        '''

        if not len(self.cursor.execute("SELECT * from Tags WHERE name = '" + \
                   str(urllib.parse.quote(str(key))) + "'").fetchall()) >= 1:
            datacpy = self.cursor.execute("SELECT count() from Tags")
            value = datacpy.fetchone()[0] + 1

            #TO DO add proper parents support

            namespace_id = self.pull_data("Namespace", "name", namespace)[0][0]
            self.cursor.execute("INSERT INTO Tags(id, name,namespace) VALUES(?, ?, ?)", \
                                (value, str(urllib.parse.quote(str(key))), namespace_id))

    def file_manager(self, hashes, filename, size, ext):
        '''
        Adds file into File table in DB
        '''

        if not len(self.cursor.execute("SELECT * from File WHERE hash = '" + \
                   str(hashes) + "'").fetchall()) >= 1:
        #if not key in self.cursor.execute("SELECT * from Namespace WHERE name = '" \
                                           #+ key + "'").fetchall()[0]:
            datacpy = self.cursor.execute("SELECT count() from File")
            value = datacpy.fetchone()[0] + 1
            self.cursor.execute("INSERT INTO File(id, hash, filename, size, ext) " + \
                                "VALUES(?, ?, ?, ?, ?)",
                                (value, hashes, filename, size, ext))
        else:
            self.hashestoignore.append(hashes)
            #self.universal.log_write.write("File Manager ignoring hash: " + str(hash))

    def t_and_f_relation_manager(self, hashes, tag):
        '''
        Handles the relationship adding of hashes and tags
        '''
        tagid = self.cursor.execute("SELECT * from Tags WHERE name = '" + \
                                    str(str(urllib.parse.quote(str(tag)))) + "'").fetchall()
        fileid = self.cursor.execute("SELECT * from File WHERE hash = '" + \
                                     str(hashes) + "'").fetchall()

        if len(tagid) == 1 and len(fileid) == 1:
            if not hashes in self.hashestoignore:
                self.cursor.execute("INSERT INTO RelationShip(fileid, tagid) " + \
                                    "VALUES(?, ?)", (fileid[0][0], tagid[0][0]))

        else:
            print("t and f error", tagid, fileid)

    def add_setting(self, name, pretty, num, param):
        self.cursor.execute("INSERT INTO Settings VALUES(?, ?, ?, ?)", (name, pretty, num, param))

    def return_count(self, table, collumn, *args):
        '''
        Returns the count of a given collumn with or without search terms
        '''
        if len(args) > 0:
            return self.cursor.execute("SELECT Count( " + str(collumn) + ") from " + str(table) + " WHERE " + str(collumn) + " = '" + str(args[0]) + "'").fetchone()[0]
        else:
            return int(self.cursor.execute("SELECT Count(*) from " + str(table)).fetchone()[0])

    def delete_data(self, table, column, search_term):
        self.cursor.execute("DELETE FROM " + str(table) + " WHERE " + str(column) + " = " + str(search_term))

    def search_tagid(self, tag_id):
        '''
        Returns the tag ids that matches the tags.
        '''
        return self.pull_data("Tags", "id", str(tag_id))

    def search_tags(self, tags):
        '''
        Returns the tag ids that matches the tags.
        '''
        return self.pull_data("Tags", "name", str(str(urllib.parse.quote(str(tags)))))

    def search_relationships(self, tagid):
        '''
        Returns the relationship between a tagid and the fileid
        '''
        return self.pull_data("RelationShip", "tagid", tagid)

    def search_relationships_file(self, file_id):
        '''
        Returns the relationship between a fileid and the tagid.
        '''
        return self.pull_data("RelationShip", "fileid", file_id)

    def direct_sqlite_return(self, data):
        '''
        Allows direct access to sqlite3 database. Is dangerous. but IDK
        '''
        return self.cursor.execute(data)

    def direct_sqlite(self, data):
        '''
        Allows direct access to sqlite3 database. Is dangerous. but IDK
        '''
        self.cursor.execute(data)

    def pull_file(self, fileid):
        '''
        Pulls file info from fileID in database
        '''
        return self.pull_data("File", "id", fileid)

    def create_default(self):
        '''
        Creates Default Database
        '''
        default_agent = "DIYHydrus/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 DIYHydrus/10.0"

        self.cursor.execute('''CREATE TABLE File(
                            id INTEGER,
                            hash text,
                            filename text,
                            size real,
                            ext text)''')

        self.cursor.execute('''CREATE TABLE Tags(
                                            id INTEGER,
                                            name text,
                                            parents INTEGER,
                                            namespace INTEGER)''')

        self.cursor.execute('''CREATE TABLE RelationShip(
                                            fileid INTEGER,
                                            tagid INTEGER)''')

        self.cursor.execute('''CREATE TABLE Parents(
                                            id INTEGER,
                                            name text,
                                            children text,
                                            namespace INTEGER)''')

        self.cursor.execute('''CREATE TABLE Namespace(
                                            id INTEGER,
                                            name text,
                                            description text)''')

        self.cursor.execute('''CREATE TABLE Settings(
                                            name text,
                                            pretty text,
                                            num INTEGER,
                                            param text)''')

        # Added in Version 1.1 for parser support
        self.cursor.execute('''CREATE TABLE Parsers(name text, url text, parser text)''')

        # Adding Current Version into DB as First Thing Done
        self.cursor.execute("INSERT INTO Settings(name, pretty, num, param) " + \
                            "VALUES(?, ?, ?, ?)", \
                            ("VERSION", None, self.VERSION, None))
        self.cursor.execute("INSERT INTO Settings(name, pretty, num, param) " + \
                            "VALUES(?, ?, ?, ?)", \
                            ("DEFAULTRATELIMIT", None, 5, None))
        self.cursor.execute("INSERT INTO Settings(name, pretty, num, param) " + \
                            "VALUES(?, ?, ?, ?)", \
                            ("FilesLoc", None, None, "Files/"))
        self.cursor.execute("INSERT INTO Settings(name, pretty, num, param) " + \
                            "VALUES(?, ?, ?, ?)", \
                            ("DEFAULTUSERAGENT", None, None, default_agent))
        self.write()

    def optimized_file_tag_pull(self, file_id):
        tag_data = self.search_relationships_file(file_id)

        _list = ""
        for each in tag_data:
            if not tag_data[-1] == each:
                _list += "id = " + str(each[1]) + " OR "
            else:
                _list += "id = " + str(each[1])


        tags = self.cursor.execute("SELECT name FROM Tags where " + _list).fetchall()
        _list = []
        for each in tags:
            _list.append(each[0])
        return _list

    def pull_all_tags_file(self, file_id):
        '''
        Pulls all tags associated with a file id.
        '''
        tag_data = self.search_relationships_file(file_id)
        _list = []
        for each in tag_data:
            _list.append(self.search_tagid(each[1])[0][1])
        return _list
    #TO DO Cache returns to here in memory for further optimizations.
    def invert_pull_data(self, table, collumn, search_term):
        '''
        Handler to return data that gets pulled from the database
        '''
        return self.cursor.execute("SELECT * from " + str(table)
                                   + " WHERE " + str(collumn)
                                   + " != '" + str(search_term)
                                   + "'").fetchall()

    #TO DO Cache returns to here in memory for further optimizations.
    def pull_data(self, table, collumn, search_term):
        '''
        Handler to return data that gets pulled from the database
        '''
        return self.cursor.execute("SELECT * from " + str(table)
                                   + " WHERE " + str(collumn)
                                   + " = '" + str(search_term)
                                   + "'").fetchall()

    def pull_scrapers(self):
        ''' Returns a list of scrapers '''
        result = self.cursor.execute("SELECT * from Settings WHERE name = 'Scraper'").fetchall()
        return result
