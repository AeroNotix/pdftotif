"""

This module deals purely with multithreading

Beyond here, be dragons. Arm yourself.

"""
import os
import time

from PyQt4.QtCore import QThread, SIGNAL, QProcess


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


class FileCleaner(QThread):

    """
    Cleans temp files
    """

    def __init__(self, deletions, cls, parent=None):

        """
        Create instance of FileCleaner with new list
        """

        super(FileCleaner, self).__init__(parent)
        self.deletions = deletions
        self.cls = cls

    def run(self):

        """
        Tasks to complete in a separate thread
        """

        time.sleep(3)
        for fname in self.deletions:
            os.remove(fname)
        try:
            self.cls.gui.pushButton.setEnabled(True)
        except AttributeError:
            pass
        self.cleanup()

    def cleanup(self):
        self.exit()

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

    def cleanup(self):
        for _thread in self.active_threads:
            _thread.exit()
            _thread.wait()
