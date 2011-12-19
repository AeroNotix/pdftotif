import sys

from PyQt4 import QtGui

from scanning_qthread.ui.ui.options_UI import Ui_Dialog


class OptionsDialog(QtGui.QDialog):

    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.gui = Ui_Dialog()
        self.gui.setupUi(self)
        self.gui.spinBox.setValue(self.parent.thread_number)

    def accept(self):
        self.hide()
        self.parent.thread_number = self.gui.spinBox.value()


if __name__ == "__main__":

    APPLICATION = QtGui.QApplication(sys.argv)
    MAINWINDOW = OptionsDialog()
    MAINWINDOW.show()
    sys.exit(APPLICATION.exec_())