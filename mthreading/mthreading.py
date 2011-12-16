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

    def run(self):

        """
        Tasks to complete in a separate thread
        """

        for fname in self.deletions:
            os.remove(fname)



class QFileWorker(object):

    def __init__(self, deletions, cls):
        """
        This class handles deletion of temporary file objects once processing
        has completed.

        It takes a reference to the class because we re-enable it's button
        because we disabled it during processing
        """

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

        This class should not be called directly as it is a QRunnable object
        therefore we need a QThreadPool object to start/stop and monitor
        progress

        The worker is QWorker and will create these instances for us.
        """

        # Init parent object
        QRunnable.__init__(self)

        # create an instance of a QObject so we can emit signals
        self.q_object = QObject()

        # take the inputs
        self.ofname = ofname
        self.ifname = ifname

        # gs exe
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

        """
        This class creates new instances of QRunner, which is the class
        that directly interfaces with the external executable

        We need to create the QRunner/QWorker routine because a QRunnable
        does not inherit from QObject and therefore does not have access
        to the signal/slot mechanisms that we need in order to receive when
        things get done.

        QWorker inherits from QObject, so we need to directly call QObjects
        constructor to initialize the underlying C++ object, super() does not
        allow for this (seemingly) so we need to call it directly.
        """

        # init QObject
        QObject.__init__(self)

        # Our own threadpool, for adding QRunners
        self.threadpool = QThreadPool()

    def create_job(self, ifname, ofname, cls):

        """
        This method takes three arguments:

        ifname is the input file name of the file to be converted
        ofname is a string which is to be the output of the filename
        cls is a reference to the calling class, so that we can connect
        a signal to a slot.
        """

        # Create the QRunner object and pass it filenames
        runner = QRunner(ifname, ofname)

        # using our own connect method inherited from QObject
        # connect the QRunner created before and use it's QObject
        # to connect a signal to the slot
        self.connect(runner.q_object, SIGNAL(
                                         "finished()"), cls.update_progress_bar)

        # ask our threadpool to run the task
        self.threadpool.start(runner)


class QThreadHandle(QRunnable):

    def __init__(self, pdf, cls):

        """
        This is the only class that gets called from the main thread

        It is called when we wish to split a PDF document and when we
        want to start a new batch of threads for image processing

        This class is a thread of it's own, controlling other threads

        I believe this is a good method as it behaves as below:

        Main thread
            |
        Call to QThreadHandle----> Start image processing
            |                               |
        Main thread carries on              |
                                         output

        Requires a PdfFileReader object and a reference to the calling class
        """

        # init parent
        QRunnable.__init__(self)

        # take refs
        self.pdf = pdf
        self.cls = cls

        # create QWorker object
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


