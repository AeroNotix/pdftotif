"""

Module for converting PDF files to tiff files en masse

"""

import os
import sys
import subprocess
import time
import threading
from Queue import Queue

from PyQt4 import QtGui
import Image, ImageFilter, ImageEnhance

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
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.gscriptpath = '"' +  os.getcwd() + r'\gs\gs9.02\bin'
        self.ui.progressBar.hide()

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


    def convert(self):

        """
        Attempted implementation of multithreaded processing
        """
        def producer(q, pdf):

            self.deletions = []
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

                thread = PDFConverter(
                            '"'  + str(
                            self.single_output_dir +
                            "\\page%s.pdf" % i +
                            '"' ).replace('/', '\\'),     # WTF IS THIS SHIT

                            str('"' +
                            self.single_output_dir +
                            "\\page%s.tif" % i +
                            '"').replace('/', '\\'))      # WTF IS THIS SHIT

                thread.start()
                q.put(thread, True)


        def consumer(q, total_files):
            finished = 0
            while finished < total_files:
                thread = q.get(True)
                thread.join()
                finished+= 1

        q = Queue(30)
        pdffname = PdfFileReader(open(self.ui.single_line_in.text(), 'rb'))

        prod_thread = threading.Thread(target=producer,
                                       args=(q, pdffname))
        cons_thread = threading.Thread(target=consumer,
                                       args=(q, pdffname.numPages))

        prod_thread.start()
        cons_thread.start()
        prod_thread.join()
        cons_thread.join()

        #cleanup(self.deletions)



#-------------------------------Helper Functions--------------------------------

def cleanup(deletions):

    """
    Deletes temporary files
    """
    for fname in deletions:
        os.remove(fname)

def encase(string, target):
    return string+target+string

#-------------------------------Multithreading----------------------------------


class PDFConverter(threading.Thread):

    """
    Multithreading offloader for converter
    """

    def __init__(self, ifname, ofname):
        self.ifname = ifname
        self.ofname = ofname
        self.gscriptpath = '"' +  os.getcwd() + r'\gs\gs9.02\bin'
        threading.Thread.__init__(self)

    def run(self):

        """
        Converts PDF pages to tif files,

        Uses ghostscript from the command line
        """

        cmd = subprocess.Popen(' '.join([
                           self.gscriptpath + '\gswin32c.exe"',   #gs exe
                           '-q',
                           '-dNOPAUSE',
                           '-dBATCH',
                           '-r900',       # resolution
                           '-sDEVICE=tiffg4',  # container type, see gs docs
                           '-sPAPERSIZE=a4',   # page size
                           '-sOutputFile=%s %s' % (str(self.ofname), str(self.ifname)),
                           ]), shell=True)  # don't spawn cmd window

        #cmd.wait()

class ProgressUpdater(threading.Thread):
    """
    Offloads updating the progress bar to a thread
    """

    def __init__(self, bar):
        self.bar = bar

    def run(self):
        bar.setValue(bar.value() + 1)


if __name__ == "__main__":
    APPLICATION = QtGui.QApplication(sys.argv)
    MAINWINDOW = MainWindow()
    MAINWINDOW.show()
    sys.exit(APPLICATION.exec_())
