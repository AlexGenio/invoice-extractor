import sys
import logging

OUTPUT_LOGGER    = logging.getLogger(__name__)
OUTPUT_FORMATTER = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
OUTPUT_COLORS = {
    logging.DEBUG: 'black',
    logging.INFO: 'blue',
    logging.WARNING: 'orange',
    logging.ERROR: 'red',
    logging.CRITICAL: 'purple',
}

class LoggerManager(object):
    """
    Creates a class that will both print and log events.
    """
    
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if LoggerManager.__instance == None:
            LoggerManager()
        return LoggerManager.__instance

    def __init__(self):
        """ Virtually private constructor. """

        OUTPUT_LOGGER.setLevel(logging.INFO)

        self.verbose = True
        self.file_handler = None

        if LoggerManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            LoggerManager.__instance = self
            sys.stdout = self

    def setVerbose(self, verbose):
        self.verbose = verbose

    def setOutputFile(self, filename):
        if self.file_handler:
            OUTPUT_LOGGER.removeHandler(self.file_handler)
            self.file_handler = None

        if filename != "":
            # create and add file handler
            self.file_handler = logging.FileHandler(filename)
            self.file_handler.setFormatter(OUTPUT_FORMATTER)
            OUTPUT_LOGGER.addHandler(self.file_handler)

    def write(self, message):
        if message != "\n":
            OUTPUT_LOGGER.log(logging.INFO, message.strip())

    def flush(self):
        pass