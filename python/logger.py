'''
logger.py writes error logs in DB file directory or Current Working Dir if not specified

'''

import datetime

class LoggerHandler():
    '''
    Handles Log Files Getting Written to disk.
    '''
    def __init__(self, Dir):
        datetime_object = datetime.datetime.now()
        self.file_handler = open(str(Dir) + str(datetime_object) + ".txt", "w")

    def __del__(self):
        '''
        Closes the log file when Logger.Handler is destroyed.
        '''
        self.file_handler.close()


    def write(self, message):
        '''
        Writes the message to log.
        '''
        self.file_handler.write(message + "\n")
