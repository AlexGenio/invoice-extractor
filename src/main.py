import sys
import resources_rc

from PyQt5 import QtWidgets, QtGui

from globals import APP_NAME, ORG_NAME
from main_window import MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(ORG_NAME)
    app.setWindowIcon(QtGui.QIcon(":/app/logo.ico"))

    main = MainWindow()
    main.setWindowIcon(QtGui.QIcon(":/app/logo.ico"))
    main.show()

    sys.exit(app.exec_())

if __name__=='__main__':
    main()