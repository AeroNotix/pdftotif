"""

Module for converting PDF files to tiff files en masse

"""

import os
import sys
import subprocess

from PyQt4 import QtGui, QtCore
from pyPdf import PdfFileWriter, PdfFileReader
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
        dir_loc = QtGui.QDir()

    def single_locate_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(
                                        self, 'Open', '' ,('PDF Files (*.pdf)'))
        self._split_pdf(filename)


    def _split_pdf(self, filename):


        inputpdf = PdfFileReader(open(filename, 'rb'))

        for i in xrange(inputpdf.numPages):

         output = PdfFileWriter()
         output.addPage(inputpdf.getPage(i))
         outputStream = open(r"C:\Documents and Settings\francea\Desktop\outputdir\NEW%s.pdf" % i, "wb")
         output.write(outputStream)
         outputStream.close()



if __name__ == "__main__":
    APPLICATION = QtGui.QApplication(sys.argv)
    MAINWINDOW = MainWindow()
    MAINWINDOW.show()
    sys.exit(APPLICATION.exec_())
