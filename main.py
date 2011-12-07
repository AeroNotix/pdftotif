"""

Module for converting PDF files to tiff files en masse

"""

import os
import sys
import subprocess
#import time
import threading
from Queue import Queue

from PyQt4 import QtGui
#import Image, ImageFilter, ImageEnhance

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


    def convert(self):

        """
        Implementation of multithreaded processing
        """
        def producer(queue, pdf):

            """
            Produces jobs for the consumer to monitor
            """

            deletions = []
            # Loop through the PDF creating a output stream
            # and putting the single page into it.
            for i in xrange(pdf.numPages):

                output = PdfFileWriter()  # output init
                output.addPage(pdf.getPage(i)) # get page index from orignal


                # append file name of the pdf to the list, so we can tidy up
                deletions.append(
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
                queue.put(thread, True)


        def consumer(queue, total_files):

            """
            Receives jobs and blocks whilst they complete
            """

            finished = 0 # task counter

            while finished < total_files:

                # get tasks
                thread = queue.get(True)

                # block whilst running
                thread.join()
                finished += 1


        # Queue size, we can play with this.
        queue = Queue(30)

        # open pdf and assign local var
        pdffname = PdfFileReader(open(self.gui.single_line_in.text(), 'rb'))

        # init threads
        prod_thread = threading.Thread(target=producer,
                                       args=(queue, pdffname))


        cons_thread = threading.Thread(target=consumer,
                                       args=(queue, pdffname.numPages))

        prod_thread.start()    # Start them engines!
        cons_thread.start()
        prod_thread.join()     # Ensure block!
        cons_thread.join()

        #cleanup(deletions)



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

        subprocess.Popen(' '.join([
                           self.gscriptpath + '\gswin32c.exe"',   #gs exe
                           '-q',
                           '-dNOPAUSE',
                           '-dBATCH',
                           '-r900',       # resolution
                           '-sDEVICE=tiffg4',  # container type, see gs docs
                           '-sPAPERSIZE=a4',   # page size
                           '-sOutputFile=%s %s' % (str(self.ofname),
                                                   str(self.ifname))

                           ]), shell=True)  # don't spawn cmd window

        #cmd.wait()



if __name__ == "__main__":
    APPLICATION = QtGui.QApplication(sys.argv)
    MAINWINDOW = MainWindow()
    MAINWINDOW.show()
    sys.exit(APPLICATION.exec_())
