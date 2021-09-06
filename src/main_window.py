import os

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox

from ui.ui_mainwindow import Ui_MainWindow

from globals import APP_NAME, ORG_NAME
from module_base import ModuleBase
from threads import ExtractorThread
from extractor_factory import ExtractorFactory
from logger_console import LoggerConsole

PATH_NOT_FOUND = "The following error has occured:\n\nThe path to {} '{}' does not exist."
FILE_OPENED    = "The following error has occured:\n\nThe output file '{}' is currently being used by another process."

class MainWindow(ModuleBase,QMainWindow):

    __DEFAULT_INVOICE_DIR_KEY = "default_invoice_dir"
    __DEFAULT_OUTPUT_DIR_KEY = "default_output_file"

    def __init__(self, parent=None):
        ModuleBase.__init__(self, __name__)
        QMainWindow.__init__(self, parent)

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.__worker_thread = None
        self.__settings = QSettings(APP_NAME, ORG_NAME)

        self.__setupAdditionalUi__()
        self.__createConnections__()

    def __setupAdditionalUi__(self):
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.ui.loggerConsole.setWidget(LoggerConsole())

    def __createConnections__(self):
        self.ui.pushButtonBrowseInvoice.clicked.connect(self.__browseInvoiceFolder__)
        self.ui.pushButtonBrowseOutput.clicked.connect(self.__browseOutputFolder__)
        self.ui.pushButtonExtract.clicked.connect(self.__extract__)

    @QtCore.pyqtSlot()
    def __browseInvoiceFolder__(self):
        default_dir = self.__settings.value(self.__DEFAULT_INVOICE_DIR_KEY,
                                            type=str)

        dialog = QFileDialog(self, "Select Invoice Directory", default_dir)
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        if dialog.exec() == QFileDialog.Accepted:
            invoice_dir = dialog.selectedFiles()[0]
            self.__settings.setValue(self.__DEFAULT_INVOICE_DIR_KEY,
                                     invoice_dir)
            self.ui.lineEditInvoiceDir.setText(invoice_dir)


    @QtCore.pyqtSlot()
    def __browseOutputFolder__(self):
        default_out_dir = self.__settings.value(self.__DEFAULT_OUTPUT_DIR_KEY,
                                                 type=str)

        dialog = QFileDialog(self, "Select Output Directory", default_out_dir)
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        if dialog.exec() == QFileDialog.Accepted:
            out_dir = dialog.selectedFiles()[0]
            self.__settings.setValue(self.__DEFAULT_OUTPUT_DIR_KEY,
                                     out_dir)
            self.ui.lineEditOutputDir.setText(out_dir)

    @QtCore.pyqtSlot()
    def __extract__(self):
        # get the configuration
        invoice_dir = self.ui.lineEditInvoiceDir.text()

        if not os.path.exists(invoice_dir):
            QMessageBox.critical(self, "Error", PATH_NOT_FOUND.format("invoice directory", invoice_dir))
            return

        output_dir = self.ui.lineEditOutputDir.text()

        if not os.path.exists(output_dir):
            QMessageBox.critical(self, "Error", PATH_NOT_FOUND.format("output directory", output_dir))
            return

        output_file = output_dir + os.sep + "ExtractionOutput.xlsx"

        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except OSError:
                QMessageBox.critical(self, "Error", FILE_OPENED.format(output_file))
                return

        # create the appropriate extractpr
        extractor_pdf = ExtractorFactory.createExtractor("pdf", invoice_dir, output_file)

        if not self.__worker_thread:
            self.__worker_thread = ExtractorThread(extractor_pdf)
            self.__worker_thread.extraction_complete.connect(self.__workerThreadCompleted__)
            self.__worker_thread.start()

    @QtCore.pyqtSlot()
    def __workerThreadCompleted__(self):
        self.__worker_thread.disconnect()
        self.__worker_thread = None