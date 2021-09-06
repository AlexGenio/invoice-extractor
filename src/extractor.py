from abc import ABC, abstractmethod

from module_base import ModuleBase
from logger_manager import LoggerManager, OUTPUT_LOGGER

class Extractor(ModuleBase, ABC, object):

    def __init__(self, module_name, root_dir, output_file):
        ModuleBase.__init__(self, module_name)

        self._root_dir       = root_dir
        self._output_file    = output_file
        self._logger_manager = LoggerManager.getInstance()

    def extract(self):
        """Recursively traverses a root directory and takes parses files
        to extract particular data and process the extracted data.
        """

        self.printHeader()

        # call on child class to perform the extraction
        self.doExtraction()

        self.printFooter()

        # call on child class to perform the post extraction processing
        self.postProcessResults()

    @abstractmethod
    def printHeader(self):
        pass

    @abstractmethod
    def doExtraction(self):
        pass

    @abstractmethod
    def postProcessResults(self):
        pass

    @abstractmethod
    def printFooter(self):
        pass