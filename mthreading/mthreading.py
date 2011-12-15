"""

This module deals purely with multithreading

Beyond here, be dragons. Arm yourself.

"""
import os
import time

from pyPdf import PdfFileWriter, PdfFileReader

from PyQt4.QtCore import (QThread, SIGNAL, QProcess,
                          QRunnable, QThreadPool, QObject)


class QFileCleaner(QRunnable):

    """
    Cleans temp files
    """

    def __init__(self, deletions, cls):

        """
        Create instance of QFileCleaner with new list
        """

        QRunnable.__init__(self)
        self.deletions = deletions
        self.cls = cls
        self.q_object = QObject()

    def run(self):

        """
        Tasks to complete in a separate thread
        """

        for fname in self.deletions:
            os.remove(fname)
        try:
            self.cls.gui.pushButton.setEnabled(True)
        except AttributeError:
            pass


class QFileWorker(QObject):

    def __init__(self, deletions, cls):
        """init attribs"""
        QObject.__init__(self)

        self.deletions = deletions
        self.threadpool = QThreadPool()
        self.cls = cls
        self._start()

    def _start(self):
        deleter = QFileCleaner(self.deletions, self.cls)
        self.threadpool.start(deleter)
        self.threadpool.waitForDone()




class QRunner(QRunnable):

    """
    Only QRunnable objects can be used with the QThreadPool
    therefore we need to do the whole song and dance with
    creating QRunnables, connecting signals and other such nonsense.
    """

    def __init__(self, ifname, ofname):
        """
        This class does the work of moving the files to the executable to
        process the pdf pages.
        """
        QRunnable.__init__(self)
        self.q_object = QObject()
        self.ofname = ofname
        self.ifname = ifname
        self.gscriptpath = '"' +  os.getcwd() + r'\gs\gs9.02\bin'

    def run(self):

        """
        Tasks to put in separate thread.
        """

        self.process_file()
        self.q_object.emit(SIGNAL("finished()"))


    def process_file(self):

        """
        Converts PDF pages to tif files,

        Uses ghostscript from the command line
        """

        process = QProcess()

        process.start(' '.join([
                           self.gscriptpath + '\gswin32c.exe"',   #gs exe
                           '-q',
                           '-dNOPAUSE',
                           '-dBATCH',
                           '-r900',            # resolution
                           '-sDEVICE=tiffg4',  # container type, see gs docs
                           '-sPAPERSIZE=a4',   # page size
                           '-sOutputFile=%s %s' % (str(self.ofname),
                                                   str(self.ifname))]))
                           # don't spawn cmd window

        process.waitForFinished(-1)


class QWorker(QObject):

    """
    Starts the QRunnable in a QThreadPool,  inherits QObject because
    we need to connect signals from the objects we are creating to
    the functions that update the UI
    """

    def __init__(self):
        """init attribs"""
        QObject.__init__(self)
        self.threadpool = QThreadPool()

    def create_job(self, ifname, ofname, cls):
        runner = QRunner(ifname, ofname)
        self.connect(runner.q_object, SIGNAL(
                                         "finished()"), cls.update_progress_bar)
        self.threadpool.start(runner)
        #self.threadpool.waitForDone()



class QThreadHandle(QRunnable):

    def __init__(self, pdf, cls):
        QRunnable.__init__(self)
        self.pdf = pdf
        self.cls = cls
        self.work = QWorker()
        self.work.threadpool.setMaxThreadCount(5)

    def run(self):


        for i in xrange(self.pdf.numPages):

            output = PdfFileWriter()  # output init
            output.addPage(self.pdf.getPage(i)) # get page index from orignal


            # append file name of the pdf to the list, so we can tidy up
            self.cls.deletions.append(
                        str(self.cls.single_output_dir +
                        "\page%s.pdf" % i).replace('/', '\\'))

            # create the output PDF file handle
            output_stream = open(
                           self.cls.single_output_dir + "\page%s.pdf" % i, "wb")


            # Write the data to the stream and close
            output.write(output_stream)
            output_stream.close()


            # Send the newly created PDF to the TIF converter.
            # Concatenates file names surrounding in quotes for CLI
            # interface to the converter.
            # Take time to expand this so you can see the filenames form.

            self.work.create_job(
                        '"'  + str(
                        self.cls.single_output_dir +
                        "\\page%s.pdf" % i +
                        '"' ).replace('/', '\\'),     # WTF IS THIS SHIT

                        str('"' +
                        self.cls.single_output_dir +
                        "\\page%s.tif" % i +
                        '"').replace('/', '\\'), self.cls)   # WTF IS THIS SHIT

            #self.work.threadpool.waitForDone()



