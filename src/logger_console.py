import logging

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QAction
from ui.ui_loggerconsole import Ui_loggerConsole

from module_base import ModuleBase
from logger_manager import OUTPUT_LOGGER, OUTPUT_FORMATTER, OUTPUT_COLORS
from ui_log_handler import UiLogHandler

class LoggerConsole(ModuleBase,QWidget):

    def __init__(self, parent=None):
        ModuleBase.__init__(self, __name__)
        QWidget.__init__(self, parent)

        # Set up the user interface from Designer.
        self.ui = Ui_loggerConsole()
        self.ui.setupUi(self)

        self.__setupAdditionalUi__()
        self.__createConnections__()

    def __setupAdditionalUi__(self):
        self.ui.plainTextEdit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.plainTextEdit.customContextMenuRequested.connect(self.__showContextMenu__)

        self.__action_clear = QAction("Clear", self)
        self.__action_clear.triggered.connect(self.__clearOutputConsole__)

    def __createConnections__(self):
        self.__ui_handler = UiLogHandler(self.log)
        self.__ui_handler.setFormatter(OUTPUT_FORMATTER)
        OUTPUT_LOGGER.addHandler( self.__ui_handler )

    def __showContextMenu__(self, location):
        self.__console_menu = self.ui.plainTextEdit.createStandardContextMenu()
        self.__console_menu.addAction(self.__action_clear)
        self.__console_menu.popup(self.mapToGlobal(location))
        
    def __clearOutputConsole__(self):
        self.ui.plainTextEdit.clear()

    @QtCore.pyqtSlot(str, logging.LogRecord)
    def log(self, status, record):
        color = OUTPUT_COLORS.get(record.levelno, 'black')
        s = '<pre><font color="%s">%s</font></pre>' % (color, status)
        self.ui.plainTextEdit.appendHtml(s)