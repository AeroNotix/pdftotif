import sys

from PyQt4 import QtGui

from scanning_qthread.ui.ui.about_UI import Ui_Dialog


class AboutDialog(QtGui.QDialog):
    """
    Creates an AboutDialog
    """

    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent)

        self.gui = Ui_Dialog()
        self.gui.setupUi(self)


if __name__ == "__main__":

    APPLICATION = QtGui.QApplication(sys.argv)
    MAINWINDOW = AboutDialog()
    MAINWINDOW.show()
    sys.exit(APPLICATION.exec_())
