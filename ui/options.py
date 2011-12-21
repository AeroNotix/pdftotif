import sys

from PyQt4 import QtGui

from scanning_qthread.ui.ui.options_UI import Ui_Dialog


class OptionsDialog(QtGui.QDialog):

    """
    Dialog that shows the options menu
    """

    def __init__(self, parent=None):

        """
        Dialog that shows the options menu
        """

        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.gui = Ui_Dialog()
        self.gui.setupUi(self)

        try:
            self.gui.spinBox.setValue(self.parent.thread_number)
        except AttributeError:
            pass


        # since we set the resolution from the dict last time
        # we can grab the number and set the index of the combo
        # box from that.
        self.previous_index = {150: 0, 300: 1,
                               450: 2, 600: 3,
                               900: 4}

        # dict map for setting resolutions on the class
        #
        # Using strings because it's much more obvious
        # what we're trying to do here.
        self.quality_dict = {'Very Low Quality': 150,
                             'Low Quality': 300,
                             'Medium Quality': 450,
                             'High Quality': 600,
                             'Very High Quality': 900}

        # apply value from dict
        try:
            self.gui.comboBox.setCurrentIndex(
                                    self.previous_index[self.parent.resolution])
        except AttributeError:
            pass


    def accept(self):

        """
        Kills the dialog
        """

        try:
            self.parent.thread_number = self.gui.spinBox.value()
        except AttributeError:
            pass

        self.done(0)

    def quality_change(self, quality):

        """
        Changes the quality setting on the GUI class
        """
        try:
            self.parent.resolution = self.quality_dict[str(quality)]
        except AttributeError:
            pass


if __name__ == "__main__":

    """
    In module testing
    """

    APPLICATION = QtGui.QApplication(sys.argv)
    MAINWINDOW = OptionsDialog()
    MAINWINDOW.show()
    sys.exit(APPLICATION.exec_())