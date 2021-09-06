import logging

from PyQt5 import QtCore

#
# Signals need to be contained in a QObject or subclass in order to be correctly
# initialized.
#
class Signaller(QtCore.QObject):
    signal = QtCore.pyqtSignal(str, logging.LogRecord)

#
# Output to a Qt GUI is only supposed to happen on the main thread. So, this
# handler is designed to take a slot function which is set up to run in the main
# thread. In this example, the function takes a string argument which is a
# formatted log message, and the log record which generated it. The formatted
# string is just a convenience - you could format a string for output any way
# you like in the slot function itself.
#
# You specify the slot function to do whatever GUI updates you want. The handler
# doesn't know or care about specific UI elements.
#
class UiLogHandler(logging.Handler):

    def __init__(self, slotfunc, *args, **kwargs):
        super(UiLogHandler, self).__init__(*args, **kwargs)
        self.__signaller = Signaller()
        self.__signaller.signal.connect(slotfunc)

    def emit(self, record):
        s = self.format(record)
        self.__signaller.signal.emit(s, record)