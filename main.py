"""

Module for converting PDF files to tiff files en masse

"""


import os
import sys


from PyQt4 import QtGui, QtCore

from scanning_tools.main_UI import Ui_MainWindow

class MainWindow(QtGui.QMainWindow):

    """
    Main window for the application

    Takes Ui_MainWindow from mainUI.py, which is automatically generated
    with pyuic4 from the UI file.
    """

    def __init__(self, parent=None):
        """Init Window"""
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


    def dir_locate(self):
        pass

    def dir_output(self):
        pass

    def single_output_file(self):
        pass

    def single_locate_file(self):
        pass


if __name__ == "__main__":
    APPLICATION = QtGui.QApplication(sys.argv)
    MAINWINDOW = MainWindow()
    MAINWINDOW.show()
    sys.exit(APPLICATION.exec_())
