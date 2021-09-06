from PyQt5 import QtCore
from PyQt5.QtCore import QThread

class ExtractorThread(QThread):

    extraction_complete = QtCore.pyqtSignal()

    def __init__(self, extractor):
        QThread.__init__(self)
        self.__extractor = extractor

    def run(self):
        if self.__extractor:
            self.__extractor.extract()
            self.extraction_complete.emit()