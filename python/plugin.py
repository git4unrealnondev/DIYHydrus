'''
Manages the plugin loading for db
'''

import os

class PluginHandler():
    '''
    Module to handle loading plugins into program.
    '''
    pluginstoload = None
    pluginstore = {}
    universal = None

    callbacks = {}
    
    callback_list = {"file_download" : [], 
                    "database_writing":[], 
                    "":[],
                    "":[],
                    "":[]}

    def __init__(self, universal):
        self.universal = universal
        self.check_plugin_dir()

        self.return_py_list()

        self.load_into_memory()

    def callback(self, callback_name, *args):
        for each in self.callback_list[callback_name]:
            each(*args)

    @staticmethod
    def check_plugin_dir():
        '''
        Checks if plugin dir exists and if it doesn't then creates dir.
        '''
        if not os.path.exists("plugins") and not os.path.isfile("plugins"):
            os.mkdir("plugins")

    def return_py_list(self):
        '''
        Sets up plugins that need to be loaded into memory
        '''
        temp_list = []
        for files in os.listdir("plugins/"):
            temp_list.append(files)
        self.pluginstoload = temp_list

    def load_into_memory(self):
        '''
        Loads python scripts into memory
        Parses the hooks from the plugins into the system
        '''
        if len(self.pluginstoload) == 0:
            print("No Plugins to load")
            return
        #This code cleans the plugins
        for each in self.pluginstoload:
            if not os.path.exists("plugins/" + each + "/main.py"):
                self.pluginstoload.pop(self.pluginstoload.index(each))
                print("Plugin: " + str(each) + \
                    " is not a valid plugin and has been removed from loading.")
                self.universal.log_write.write("Plugin: " + str(each) + \
                    " is not a valid plugin and has been removed from loading.")
        print("PLUGINSTOLOAD: ", self.pluginstoload)
        
        #Checks if plugins are in DB run list.
        #for each in self.pluginstoload:
        plugin_check_list = self.universal.databaseRef.pull_data("Settings", "name", "PluginLoadsCheck")

        plugin_check_list_cleaned = []
        # Parses the already approved settings.
        for each in plugin_check_list:
            plugin_check_list_cleaned.append(each[3])

        plugins_not_approved = set(self.pluginstoload) - set(plugin_check_list_cleaned)
        
        for each in plugins_not_approved:
            print("PLUGIN: ", each, "Has not been approved yet! Approve (y or n)")
            user_input = ""
            while(True):
                user_input = input(": ")
                if user_input.upper() == "Y" or user_input.upper() == "N":
                    break
            if user_input.upper() == "N":
                self.pluginstoload.pop(self.pluginstoload.index(each))
            else:
                self.universal.databaseRef.add_setting("PluginLoadsCheck", None, None, str(each))

        if len(self.pluginstoload) == 0:
            return
        self.universal.log_write.write("Loading Plugins: " + str(self.pluginstoload))
        for each in self.pluginstoload:
            self.init_plugin(self.load_file("plugins/" + each + "/main.py"), each)
        for each in self.pluginstore:
            intersection = self.pluginstore[each][1].keys() & self.callback_list.keys()
            for every in intersection:
                self.callback_list[every].append(self.pluginstore[each][1][every])
            #for every in self.pluginstore[each]:
            #    print(every)
    def init_plugin(self, script_string, script_name):
        '''
        Executes plugins to read hookins
        '''
        calls = {}
        exec(script_string, {"universal": self.universal}, calls)
        self.pluginstore[script_name] = [calls["storage"], calls["hooks"]]
    
    @staticmethod
    def load_file(filename):
        '''
        Reads Plugin into Memory
        '''
        script_string = ""

        #Reads script into memory
        with open(filename, "r") as infile:
            for each in infile:
                script_string += each + "\n"
                
        return script_string
                
