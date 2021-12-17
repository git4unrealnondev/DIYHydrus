'''
logger.py writes error logs in DB file directory or Current Working Dir if not specified

'''

from datetime import datetime

class LoggerHandler():
    '''
    Handles Log Files Getting Written to disk.
    '''
    def __init__(self, Dir):
        self.datetime_object = datetime.now()

        self.file_handler = open(str(Dir) + str(self.datetime_object) + ".txt", "w")

    def __del__(self):
        '''
        Closes the log file when Logger.Handler is destroyed.
        '''
        self.file_handler.close()


    def write(self, message):
        '''
        Writes the message to log.
        '''
        self.file_handler.write(str(str(datetime.now()) + ": " + str(message) + "\n"))
