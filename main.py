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
from PyQt4.QtCore import QThreadPool

from pyPdf import PdfFileReader

from scanning_qthread.ui.main_UI import Ui_MainWindow
from scanning_qthread.mthreading.mthreading import QFileWorker, QThreadHandle

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
        self.work = QThreadPool()
        self.work.setMaxThreadCount(1)

    def quit(self):

        """
        Quit the window, in case we need some specific behaviour
        """

        print self

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

        # Create the file lookup dialog using built-in dialogs
        # We set the file type to PDF and only PDF
        self.gui.single_line_in.setText(QtGui.QFileDialog.getOpenFileName(
                                       self, 'Open', '' ,('PDF Files (*.pdf)')))


    def update_progress_bar(self):

        """
        Method to update progress bar whilst running conversion
        """

        # When we get a call it's from a thread finishing
        # we increment the progress bar and check if we're at 100%
        self.gui.progressBar.setValue(self.gui.progressBar.value()+1)

        # This is bad, if a QProcess fails, we don't get a tick
        # and the progressBar will never get to 100%
        # we need to implement something that will catch errors with
        # QProcess
        if self.gui.progressBar.value() == self.gui.progressBar.maximum():
            self.gui.progressBar.hide()

            # create the deleter thread with a reference to the deletions
            # list.
            deleter = QFileWorker(self.deletions, self)

            # wait for the deletions thread to return
            deleter.threadpool.waitForDone()

            # re-init deletions list so we don't try to delete
            # already deleted files next time
            self.deletions = []

            # Re-enable the button
            self.gui.btn_single_convert.setEnabled(True)


    def convert(self):

        """
        Implementation of multithreaded processing
        """
        self.gui.btn_single_convert.setEnabled(False) # disable button
        self.gui.progressBar.setValue(0) # re-init progress bar


        # Open the PDF that we found in the dialog
        pdf = PdfFileReader(open(self.gui.single_line_in.text(), 'rb'))

        # Show the progress bar
        self.gui.progressBar.show()

        # Set the progress bar's maximum number to the number of pages
        # in the PDF
        self.gui.progressBar.setMaximum(pdf.numPages)

        # Send the PDF object (PdfFileReader) to the ThreadHandler
        # along with a reference to ourself in order to set up signal
        # callbacks

        # most of the magic is in mthreading.py
        # this is the cleanest interface I could come up with
        # just pass it an opened PDF document and processing will begin
        self.work.start(QThreadHandle(pdf, self))


    def convert_dir(self):
        """
        Method to convert a whole directory
        """
        pass




if __name__ == "__main__":


    APPLICATION = QtGui.QApplication(sys.argv)
    MAINWINDOW = MainWindow()
    MAINWINDOW.show()
    sys.exit(APPLICATION.exec_())

