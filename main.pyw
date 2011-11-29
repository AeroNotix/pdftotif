"""

Module for converting PDF files to tiff files en masse

"""

import os
import sys
import subprocess
import time
import random

from PyQt4 import QtGui
from pyPdf import PdfFileWriter, PdfFileReader
from scanning_tools.main_UI import Ui_MainWindow

def cleanup(deletions):

    """
    Deletes temporary files
    """
    for fname in deletions:
        os.remove(fname)

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
        self.gscriptpath = '"' +  os.getcwd() + r'\gs\gs9.02\bin'

    def dir_locate(self):
        """
        Will locate a dir to split all pdfs
        """
        pass

    def dir_output(self):
        """
        Will locate an output dir for dir conversion
        """
        pass

    def single_output_file(self):

        """
        Spawns a find file dialog
        """

        self.dir_dialog = QtGui.QFileDialog(self)
        self.dir_dialog.setFileMode(QtGui.QFileDialog.Directory)

        if self.dir_dialog.exec_() == True:
            for item in self.dir_dialog.selectedFiles():
                self.single_output_dir = item
                self.ui.single_line_out.setText(item)
                break



    def single_locate_file(self):

        """
        creates a dialog to find a single file
        """

        self.ui.single_line_in.setText(QtGui.QFileDialog.getOpenFileName(
                                       self, 'Open', '' ,('PDF Files (*.pdf)')))


    def _split_pdf(self, filename):

        """
        Takes PDF file, splits it and sends each to the converter
        """

        self.deletions = []  # init deletions list

        inputpdf = PdfFileReader(open(filename, 'rb')) # open filename
                                                       # found in dialog

        # Loop through the PDF creating a output stream
        # and putting the single page into it.

        for i in xrange(inputpdf.numPages):
            print inputpdf.numPages

            output = PdfFileWriter()  # output init
            output.addPage(inputpdf.getPage(i)) # get page index from orignal


            # append file name of the pdf to the list, so we can tidy up
            self.deletions.append(
                        str(self.single_output_dir +
                        "\page%s.pdf" % i).replace('/', '\\'))

            # create the output PDF file handle
            output_stream = open(
                               self.single_output_dir + "\page%s.pdf" % i, "wb")


            # Write the data to the stream and close
            output.write(output_stream)
            output_stream.close()


            # Send the newly created PDF to the TIF converter.
            # Concatenates file names surrounding in quotes for CLI
            # interface to the converter.
            # Take time to expand this so you can see the filenames form.
            self.pdf_to_tif(
                        '"'  + str(
                        self.single_output_dir +
                        "\\page%s.pdf" % i +
                        '"' ).replace('/', '\\'),

                        str('"' +
                        self.single_output_dir +
                        "\\page%s.tif" % i +
                        '"').replace('/', '\\'))

        time.sleep(5)  # sleep to let conversion take place

        # Deletions list gets sent to the function to clear them.

        cleanup(self.deletions)

    def pdf_to_tif(self, ifname, ofname):

        """
        Converts PDF pages to tif files,

        Uses ghostscript from the command line
        """




        subprocess.Popen(' '.join([
                           self.gscriptpath + '\gswin32c.exe"',   #gs exe
                           '-q',
                           '-dNOPAUSE',
                           '-dBATCH',
                           '-r300',       # resolution
                           '-sDEVICE=tiffg4',  # container type, see gs docs
                           '-sPAPERSIZE=a4',   # page size
                           '-sOutputFile=%s %s' % (str(ofname), str(ifname)),
                           ]), shell=True)  # don't spawn cmd window


    def convert(self):

        """
        Sends PDF file to the splitter
        """

        self._split_pdf(self.ui.single_line_in.text())

if __name__ == "__main__":
    APPLICATION = QtGui.QApplication(sys.argv)
    MAINWINDOW = MainWindow()
    MAINWINDOW.show()
    sys.exit(APPLICATION.exec_())
