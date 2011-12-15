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
import time

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, QThreadPool, QReadWriteLock

from pyPdf import PdfFileReader

from scanning_qthread.ui.main_UI import Ui_MainWindow
from scanning_qthread.mthreading.mthreading import (QRunner,
                                                   QWorker,
                                                   QFileCleaner,
                                                   QFileWorker,
                                                   QThreadHandle)

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
        self.lock = QReadWriteLock()

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

        self.lock.lockForRead()
        curr_progress = self.gui.progressBar.value() + 1
        print self.gui.progressBar.value()
        self.lock.unlock()

        self.lock.lockForWrite()
        self.gui.progressBar.setValue(curr_progress)
        self.lock.unlock()

        APPLICATION.processEvents()



        if self.gui.progressBar.value() == self.gui.progressBar.maximum():
            self.gui.progressBar.hide()
            deleter = QFileWorker(self.deletions, self)
            deleter.threadpool.waitForDone()
            self.deletions = []


    def convert(self):

        """
        Implementation of multithreaded processing
        """
        self.gui.btn_dir_convert.setEnabled(False) # disable button
        self.gui.progressBar.setValue(0) # re-init progress bar
        pdf = PdfFileReader(open(self.gui.single_line_in.text(), 'rb'))

        self.gui.progressBar.show()
        self.gui.progressBar.setMaximum(pdf.numPages)

        APPLICATION.processEvents()

        start = time.clock() # debug

        work = QThreadPool()
        work.setMaxThreadCount(1)
        work.start(QThreadHandle(pdf, self))

        print time.clock() - start # debug

    def convert_dir(self):
        pass




if __name__ == "__main__":
    APPLICATION = QtGui.QApplication(sys.argv)
    MAINWINDOW = MainWindow()
    MAINWINDOW.show()
    sys.exit(APPLICATION.exec_())
