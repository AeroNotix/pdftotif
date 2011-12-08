"""

Module for converting PDF files to tiff files en masse

"""


#---------------------------Imports---------------------------------------------
import os
import sys
import subprocess
import time
#import threading
#from Queue import Queue

from PyQt4 import QtGui
from PyQt4.QtCore import QThread, SIGNAL

from pyPdf import PdfFileWriter, PdfFileReader
from scanning_tools.main_UI import Ui_MainWindow

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
            self.file_cleaner = FileCleaner(self.deletions)
            self.file_cleaner.start()


    def convert(self):

        """
        Implementation of multithreaded processing
        """

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

##        for _thread in self.threads:
##            self.connect(_thread, SIGNAL("finished(bool)"),
##                         self.update_progress_bar)
##            _thread.start()


        # Loop through QPDFConverter instances and add them to thread queue
        for _thread in self.threads:
            self.thread_handler.add_thread(_thread, self)

        # Once all are added, start queue
        self.thread_handler.start()



#-------------------------------Helper Functions--------------------------------

def cleanup(deletions):

    """
    Deletes temporary files
    """
    for fname in deletions:
        os.remove(fname)

def encase(string, target):
    """
    Encases a string in another string
    """
    return string+target+string

#-------------------------------Multithreading----------------------------------

class QPDFConverter(QThread):

    """
    Class for handling conversion of PDF files in separate threads
    """

    def __init__(self, ifname, ofname, parent=None):

        """
        Create instance for conversion
        """

        super(QPDFConverter, self).__init__(parent)
        self.ofname = ofname
        self.ifname = ifname
        self.gscriptpath = '"' +  os.getcwd() + r'\gs\gs9.02\bin'
        self.completed = False


    def run(self):

        """
        Tasks to put in separate thread.
        """

        self.process_file()
        self.emit(SIGNAL("finished(bool)"), self.completed)

    def process_file(self):

        """
        Converts PDF pages to tif files,

        Uses ghostscript from the command line
        """

        subprocess.call(' '.join([
                           self.gscriptpath + '\gswin32c.exe"',   #gs exe
                           '-q',
                           '-dNOPAUSE',
                           '-dBATCH',
                           '-r900',            # resolution
                           '-sDEVICE=tiffg4',  # container type, see gs docs
                           '-sPAPERSIZE=a4',   # page size
                           '-sOutputFile=%s %s' % (str(self.ofname),
                                                   str(self.ifname))
                           ]), shell=False)  # don't spawn cmd window

        self.completed = True



class FileCleaner(QThread):

    """
    Cleans temp files
    """

    def __init__(self, deletions, parent=None):

        """
        Create instance of FileCleaner with new list
        """

        super(FileCleaner, self).__init__(parent)
        self.deletions = deletions

    def run(self):

        """
        Tasks to complete in a separate thread
        """

        time.sleep(5)
        for fname in self.deletions:
            os.remove(fname)

class ThreadHandler(QThread):

    """
    Supposed to be handling starting and stopping of threads
    """

    def __init__(self, parent=None):
        super(ThreadHandler, self).__init__(parent)
        self.new_threads = []
        self.active_threads = []
        self.running = False

    def add_thread(self, thread, cls):

        """
        Add a new thread to the unactive queue
        """

        self.connect(thread, SIGNAL("finished(bool)"),
                     cls.update_progress_bar)
        self.new_threads.append(thread)

    def run(self):

        """
        Method to execute magic in separate threads
        """

        if not self.running:   # if we get called whilst we're running, no go!
            self.running = True    # We've started

            while self.running:
                try:
                    for i in range(len(self.new_threads)): # count threads and
                                                           # go for that long

                        # append a thread to the active list
                        self.active_threads.append(self.new_threads[i])

                        # start said thread
                        self.active_threads[i].start()

                    # wait until all threads in queue have finished.
                    while not self.threadcheck(i):
                        pass

                # if we go too far, we've ended the queue
                finally:
                    self.running = False

    def threadcheck(self, index):

        """
        Queries threads to see if they're active
        if all have ended, return true. Else false
        """

        # loop through active threads
        for _thread in self.active_threads:

            # check if threads in queue have finished
            if not _thread.isFinished():
                return False

        # if the current index is at the end, we can stop adding threads
        if index == len(self.active_threads):
            self.running = False
        return True


if __name__ == "__main__":
    APPLICATION = QtGui.QApplication(sys.argv)
    MAINWINDOW = MainWindow()
    MAINWINDOW.show()
    sys.exit(APPLICATION.exec_())
