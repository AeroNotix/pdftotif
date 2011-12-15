import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class QRunner(QRunnable):

    def __init__(self):
        super(QRunner, self).__init__()
        self.QObj = QObject()


    def run(self):

        self.QObj.emit(SIGNAL("finished()"))


class Worker(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.threadpool = QThreadPool()


    def work(self):
        for x in range(3):
            runner = QRunner()
            self.connect(runner.QObj, SIGNAL("finished()"), self.func)
            self.threadpool.start(runner)

    def func(self):
        print 'lol'


Work = Worker()

Work.work()
Work.work()
Work.work()
Work.work()
Work.work()
Work.work()
Work.work()
Work.work()