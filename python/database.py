'''
database.py Interacts With Sqlite3 Database.
'''

import sqlite3
import sys
import os
import numpy as np
import urllib.parse

import python.global_vars as universal

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
        self.conn = sqlite3.connect(str(directory) + 'main.db', check_same_thread=False)
        #self.conn = sqlite3.connect(str(directory) + 'main.db')
        self.cursor = self.conn.cursor()
        #self.cursor.execute("VACUUM")

        #Begins Transaction handling
        self.conn.execute('BEGIN')

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

    def return_working_dir(self):
        '''
        Really lazy solution am sorry.
        Their's probably a better place to put this...
        '''
        return os.getcwd()

    def tag_relationship_checker(self):
        pass
        yet = '''namespace_id = self.return_count("Namespace", "id")
        print(namespace_id)
        for each in range(1, namespace_id + 1):
            tag = self.pull_data("Tags", "namespace", each)
            for each in tag:
                relationship = self.universal.databaseRef.search_relationships(each[0])
                if each == 21:
                    print("F", each, relationship, type(relationship))'''

    def db_sanity(self):
        '''
        Checks Database sanity and ensures that Database is the same version as the others.
        '''

        self.update_loaded_db()

        result = self.cursor.execute("SELECT * from Settings WHERE name = 'VERSION'").fetchone()
        if int(result[2]) < self.VERSION:
            self.db_update(result[2], self.VERSION)
        elif int(result[2]) == self.VERSION:
            self.universal.log_write.write("Database is Up To Date")
            print("Database is Up To Date")
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

        #Checking for any errant errors in db
        self.tag_relationship_checker()

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
        namespace = self.pull_data("Namespace", "name", str(urllib.parse.quote(str(key))))
        if not len(namespace) >= 1:
        #if not len(self.cursor.execute("SELECT * from Namespace WHERE name = '" + \
        #                               str(urllib.parse.quote(str(key))) + "'").fetchall()) >= 1:
        #if not key in self.cursor.execute("SELECT * from Namespace WHERE name = '" + \
                                           #key + "'").fetchall()[0]:
            #datacpy = self.cursor.execute("SELECT count() from Namespace")
            datacpy = self.return_count("Namespace", "id", None)
            value = datacpy + 1
            #self.memorydb["Namespace"].append((str(value), str(urllib.parse.quote(str(key))), ""))
            #self.memorydb["Namespace"] = np.append(self.memorydb["Namespace"], [[int(value), str(urllib.parse.quote(str(key))),""]], axis=0)
            try:
                self.memorydb["Namespace"] = np.vstack([self.memorydb["Namespace"], [str(value), str(urllib.parse.quote(str(key))),""]])
            except ValueError as E:
                print("making namespace array")
                self.memorydb["Namespace"] = np.array([[str(value), str(urllib.parse.quote(str(key))),""]])


            self.cursor.execute("INSERT INTO Namespace(id, name, description) VALUES(?, ?, ?)", \
                                (value, str(urllib.parse.quote(str(key))), ""))
            datacpy = self.return_count("Namespace", "id", None)

    def tag_namespace_manager(self, key, namespace):
        '''
        Same as namespace_manager but with slightly more advanced logic.
        ONLY ADDS NEW x IF NOT PRESENT IN TAGS.
        '''

        tags = self.pull_data("Tags", "name", str(urllib.parse.quote(str(key))))

        if not len(tags) >= 1:
            #datacpy = self.cursor.execute("SELECT count() from Tags")
            datacpy = self.return_count("Tags", "id", None)
            value = datacpy + 1

            #TO DO add proper parents support

            namespace_id = self.pull_data("Namespace", "name", namespace)[0][0]
            #self.memorydb["Tags"] = np.append(self.memorydb["Tags"], [[str(value), str(urllib.parse.quote(str(key))), str(namespace_id)]], axis=0)

            try:
                self.memorydb["Tags"] = np.vstack([self.memorydb["Tags"], [str(value), str(urllib.parse.quote(str(key))), str(namespace_id)]])
            except ValueError as E:
                self.memorydb["Tags"] = np.array([[str(value), str(urllib.parse.quote(str(key))), str(namespace_id)]])
            self.cursor.execute("INSERT INTO Tags(id, name,namespace) VALUES(?, ?, ?)", \
                                (value, str(urllib.parse.quote(str(key))), namespace_id))

    def file_manager(self, hashes, filename, size, ext):
        '''
        Adds file into File table in DB
        '''

        storage = self.pull_data("File", "hash", str(hashes))
        if not len(storage) >= 1:
            #datacpy = self.cursor.execute("SELECT count() from File")
            datacpy = self.return_count("File", "id", None)
            value = datacpy + 1
            #self.memorydb["File"] = np.append(self.memorydb["File"], [[str(value), str(hashes), str(filename), str(size), str(ext)]], axis=0)
            try:
                self.memorydb["File"] = np.vstack([self.memorydb["File"], [[str(value), str(hashes), str(filename), str(size), str(ext)]]])
            except ValueError as E:
                self.memorydb["File"] = np.array([[str(value), str(hashes), str(filename), str(size), str(ext)]])
            self.cursor.execute("INSERT INTO File(id, hash, filename, size, ext) " + \
                                "VALUES(?, ?, ?, ?, ?)",
                                (value, hashes, filename, size, ext))
        else:
            self.hashestoignore.append(hashes)
            #self.universal.log_write.write("File Manager ignoring hash: " + str(hash))

    def update_loaded_db(self):
        '''
        Loads DB into memory. Makes reading faster
        '''
        self.memorydb = {}
        self.memorydb["Tags"] = np.array(self.cursor.execute("SELECT * from Tags").fetchall())
        self.memorydb["File"] = np.array(self.cursor.execute("SELECT * from File").fetchall())
        self.memorydb["Namespace"] = np.array(self.cursor.execute("SELECT * from Namespace").fetchall())
        self.memorydb["Settings"] = np.array(self.cursor.execute("SELECT * from Settings").fetchall())
        self.memorydb["RelationShip"] = np.array(self.cursor.execute("SELECT * from RelationShip").fetchall())

    def t_and_f_relation_manager(self, hashes, tag):
        '''
        Handles the relationship adding of hashes and tags
        '''
        tagid = self.pull_data("Tags", "name", str(urllib.parse.quote(str(tag))))
        fileid = self.pull_data("File", "hash", hashes)
        #tagid = self.cursor.execute("SELECT * from Tags WHERE name = '" + \
        #                            str(str(urllib.parse.quote(str(tag)))) + "'").fetchall()
        #fileid = self.cursor.execute("SELECT * from File WHERE hash = '" + \
        #                             str(hashes) + "'").fetchall()

        if len(tagid) == 1 and len(fileid) == 1:
            if not hashes in self.hashestoignore:
                try:
                    self.memorydb["RelationShip"] = np.vstack([self.memorydb["RelationShip"], [[str(fileid[0][0]), str(tagid[0][0])]]])
                except ValueError as E:
                    self.memorydb["RelationShip"] = np.array([str(fileid[0][0]), str(tagid[0][0])])
                #self.memorydb["RelationShip"].append((str(fileid[0][0]), str(tagid[0][0])))
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
        return len(self.memorydb[table])

    def delete_data(self, table, column, search_term):
        self.cursor.execute("DELETE FROM " + str(table) + " WHERE " + str(column) + " = " + str(search_term))

    def search_tagid(self, tag_id):
        '''
        Returns the tag ids that matches the tags.
        '''
        return self.pull_data("Tags", "id", int(tag_id))

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

    def optimized_file_tag_pull(self, table, collumn, file_id):
        tag_data = self.search_relationships_file(file_id)

        _list = ""
        for each in tag_data:
            if not tag_data[-1] == each:
                _list += "id = " + str(each[1]) + " OR "
            else:
                _list += "id = " + str(each[1])

        tags = self.pull_data(table, collumn, _list)
        #tags = self.cursor.execute("SELECT " + collumn + " FROM " + table + " where " + _list).fetchall()
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
    def pull_data(self, table, collumn, search_term, *args):
        '''
        Handler to return data that gets pulled from the database
        Now loads stuffs into memory at an insane rate. Very fast much wow.
        '''

        #Sets custom memdb location for usage with inheriting db
        custom_db = False
        if len(args) > 0:
            custom_db = True


        id = None
        search_dict = {
        "File": {"id": 0, "hash": 1, "filename": 2, "size": 3, "ext": 4},
        "RelationShip": {"fileid": 0, "tagid": 1},
        "Tags": {"id": 0, "name": 1, "parents": 2, "namespace": 3},
        "Settings": {"name": 0, "pretty": 1, "num": 2, "param": 3},
        "Namespace": {"id": 0, "name": 1, "description": 2}
        }
        if table in search_dict:
            if custom_db:
                 return_to_parse = args[0][table]
            else:
                return_to_parse = self.memorydb[table]
            to_return = []

            if search_term is None:
                return return_to_parse

            #if not search_term in return_to_parse:
            #    print()

            for each in return_to_parse:
                if isinstance(search_term, list):
                    for every in search_term[search_dict[table][collumn]]:
                        #print(search_dict[table][collumn], each, search_term)
                        if each[search_dict[table][collumn]] == every:
                            to_return.append(each)
                else:

                    try:
                        if each[search_dict[table][collumn]] == search_term :
                            to_return.append(each)
                    except Exception as E:
                        continue
            return to_return

        else:
            #This makes the DB be memory only. Not relying on disk. everything
            #in memory should be same with disk.
            if not custom_db:
                pull = self.cursor.execute("SELECT * from " + str(table)
                    + " WHERE " + str(collumn)
                    + " = '" + str(search_term)
                    + "'").fetchall()
                print("Pulling From DB", pull, str(table), str(collumn), str(search_term))
                return pull
            else:
                return {}

    def pull_scrapers(self):
        ''' Returns a list of scrapers '''
        result = self.cursor.execute("SELECT * from Settings WHERE name = 'Scraper'").fetchall()
        return result

    def inherit_db(self, temp_db_location):
        """
        Inherits data from external database into ours.
        TODO Finish program data sucking from another db. am lazy.
        """
        if os.path.exists(temp_db_location):
            external_conn = sqlite3.connect(str(temp_db_location), check_same_thread=False)
            external_cursor = external_conn.cursor()
        else:
            print("Cannot find external database did you type the location correctly?")
            self.universal.log_write.write("Cannot find external database did you type the location correctly? : "+\
                temp_db_location)
            return

        print("Pulling Data from external database. May take a moment.")

        #Creates a custom memorydb to reuse "high" quality code so i dont have to deal with custom sqlite
        memorydb = {}
        memorydb["Tags"] = external_cursor.execute("SELECT * from Tags").fetchall()
        memorydb["File"] = external_cursor.execute("SELECT * from File").fetchall()
        memorydb["Namespace"] = external_cursor.execute("SELECT * from Namespace").fetchall()
        memorydb["Settings"] = external_cursor.execute("SELECT * from Settings").fetchall()
        memorydb["RelationShip"] = external_cursor.execute("SELECT * from RelationShip").fetchall()

        #This is a read only op. Closing to preserve memory
        external_conn.close()

        current_table = self.pull_data("File", "hash", None)
        if universal.verbose:
            print("File table", len(memorydb["File"]))
            print("Currently Loaded", len(current_table))

        minus_list= set(memorydb["File"]) - set(current_table.flatten())
        print("Need to import", len(minus_list), "files.")

        namespace_mapping = {}
        for each in memorydb["Namespace"]:

            #Created a new namespace if it doesn't exist inside current database
            try:
                print(each[0], each[1])
                namespace_mapping[each[0]] = self.pull_data("Namespace", "name", each[1])[0][1]
            except IndexError as E:
                self.namespace_manager(each[1])

                namespace_mapping[each[0]] = self.pull_data("Namespace", "name", each[1])[0][1]

        cnt = 0

        print("Namespace_manager;", namespace_mapping)
        thread_num = self.universal.ThreadManager.THREAD_POOL_SIZE
        thread_work = {}
        print(thread_num)
        for i in range(0, thread_num):
            thread_work[i] = []
        print(thread_work)
        tcnt=0
        for each in minus_list:
            thread_work[tcnt].append(each)

            if tcnt == thread_num - 1:
                tcnt = 0
            else:
                tcnt += 1

        print("Creating file and tag with namespace info")

        for each in minus_list:
            self.universal.log_write.write("Adding from external db " +str( temp_db_location) + "hash:" + str(each[1]))
            self.file_manager( each[1], each[2], None, each[3])
            for rel in self.pull_data("RelationShip", "fileid", each[0], memorydb):
                self.tag_namespace_manager( self.pull_data("Tags", "id", rel[1], memorydb)[0][1], namespace_mapping[self.pull_data("Tags", "id", rel[1], memorydb)[0][3]])

        print("Completed moving to IO / CPU bound relationship tasks")

        for each in thread_work.keys():
            self.universal.ThreadManager.multiprocessing_pool(self.import_threaded(thread_work[each], memorydb, namespace_mapping))

            #print(self.pull_data("RelationShip", "fileid", each[0], memorydb))
            #print("Importing database entry:", cnt, "hash", each[1])


            #self.file_manager( each[1], each[2], None, each[3])

            ##For each relationship add tag with namespace and then
            #for rel in self.pull_data("RelationShip", "fileid", each[0], memorydb):
            #    self.tag_namespace_manager( self.pull_data("Tags", "id", rel[1], memorydb)[0][1], namespace_mapping[self.pull_data("Tags", "id", rel[1], memorydb)[0][3]])
            #    self.t_and_f_relation_manager(each[1], self.pull_data("Tags", "id", rel[1], memorydb)[0][1])

    def import_threaded(self, file_work, memorydb, namespace_mapping):
        for each in file_work:
            #self.file_manager( each[1], each[2], None, each[3])
            for rel in self.pull_data("RelationShip", "fileid", each[0], memorydb):
                #self.tag_namespace_manager( self.pull_data("Tags", "id", rel[1], memorydb)[0][1], namespace_mapping[self.pull_data("Tags", "id", rel[1], memorydb)[0][3]])
                self.t_and_f_relation_manager(each[1], self.pull_data("Tags", "id", rel[1], memorydb)[0][1])
