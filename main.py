"""

Main Module for converting PDF files to tiff files en masse

Consider breaking out into different modules, all this one really needs to do
is construct the GUI class. Everything can be imported to save on readability
and code portability. Multithreading in particular has a class that could
be beneficial elsewhere.

"""


#---------------------------Imports---------------------------------------------
import os
import sys

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

from pyPdf import PdfFileWriter, PdfFileReader
from scanning_qthread.ui.main_UI import Ui_MainWindow
from scanning_qthread.mthreading.mthreading import (QPDFConverter,
                                                   ThreadHandler,
                                                   FileCleaner)

from scanning_qthread.misc.misc import encase, cleanup

#---------------------------GUI Class-------------------------------------------

class MainWindow(QtGui.QMainWindow):

    """
    Main window for the application

    Takes Ui_MainWindow from mainUI.py, which is automatically generated
    with pyuic4 from the UI file.
    """

    def __init__(self, parent=None):
        """Init Window"""
        QtGui.QMainWindow.__init__(self, parent)
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.gscriptpath = '"' +  os.getcwd() + r'\gs\gs9.02\bin'
        self.gui.progressBar.hide()
        self.single_output_dir = ''
        self.threads = []
        self.deletions = []
        self.thread_handler = ThreadHandler()

    def quit(self):
        print 'quitted'

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

        dir_dialog = QtGui.QFileDialog(self)
        dir_dialog.setFileMode(QtGui.QFileDialog.Directory)

        if dir_dialog.exec_() == True:
            for item in dir_dialog.selectedFiles():
                self.single_output_dir = item
                self.gui.single_line_out.setText(item)
                break



    def single_locate_file(self):

        """
        creates a dialog to find a single file
        """

        self.gui.single_line_in.setText(QtGui.QFileDialog.getOpenFileName(
                                       self, 'Open', '' ,('PDF Files (*.pdf)')))


    def update_progress_bar(self):

        """
        Method to update progress bar whilst running conversion
        """

        self.gui.progressBar.setValue(self.gui.progressBar.value()+1)

        if self.gui.progressBar.value() == self.gui.progressBar.maximum():
            self.gui.progressBar.hide()
            self.file_cleaner = FileCleaner(self.deletions, self)
            self.file_cleaner.start()
            self.thread_handler.cleanup()
            self.thread_handler.exit()

    def convert(self):

        """
        Implementation of multithreaded processing
        """
        self.gui.pushButton.setEnabled(False)
        pdf = PdfFileReader(open(self.gui.single_line_in.text(), 'rb'))

        self.gui.progressBar.show()
        self.gui.progressBar.setMaximum(pdf.numPages)

        # Loop through the PDF creating a output stream
        # and putting the single page into it.

        for i in xrange(pdf.numPages):

            output = PdfFileWriter()  # output init
            output.addPage(pdf.getPage(i)) # get page index from orignal


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

            self.threads.append(QPDFConverter(
                        '"'  + str(
                        self.single_output_dir +
                        "\\page%s.pdf" % i +
                        '"' ).replace('/', '\\'),     # WTF IS THIS SHIT

                        str('"' +
                        self.single_output_dir +
                        "\\page%s.tif" % i +
                        '"').replace('/', '\\')))     # WTF IS THIS SHIT


        # Loop through QPDFConverter instances and add them to thread queue
        for _thread in self.threads:
            self.thread_handler.add_thread(_thread, self)

        # Once all are added, start queue
        self.thread_handler.start()

    def convert_dir(self):
        pass




if __name__ == "__main__":
    APPLICATION = QtGui.QApplication(sys.argv)
    MAINWINDOW = MainWindow()
    MAINWINDOW.show()
    sys.exit(APPLICATION.exec_())
