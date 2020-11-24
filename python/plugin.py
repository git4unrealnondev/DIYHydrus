'''
Manages the plugin loading for db
'''

import os
import glob

#import python.global_vars as universal

class PluginHandler():
    '''
    Module to handle loading plugins into program.
    '''
    pluginstoload = None

    def __init__(self):
        self.check_plugin_dir()

        self.return_py_list()

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
        for files in glob.glob("plugins/*.py"):
            temp_list.append(files)
        self.pluginstoload = temp_list
