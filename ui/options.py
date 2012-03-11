"""
Module for pulling the options_UI dialog form into it's own class
so we can just import that and not all the UI elements
"""

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

        # set the thread value to the value used on the parent
        try:
            self.gui.spin_Threads.setValue(self.parent.thread_number)
        except AttributeError:
            pass

        # create a map to return previous values to the dialog
        self.mode_dict = {'tiffcrle': 0,
                          'tiffg3': 1,
                          'tiffg4': 2,
                          'tifflzw': 3,
                          'tiffpack': 4}

        # set previous values on dialog
        self.gui.cmb_Mode.setCurrentIndex(self.mode_dict[self.parent.mode])


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
            self.gui.cmb_Quality.setCurrentIndex(
                                    self.previous_index[self.parent.resolution])
        except AttributeError:
            pass

#----------------------------------SLOTS----------------------------------------
    def accept(self):

        """
        Kills the dialog
        """

        try:
            self.parent.thread_number = self.gui.spin_Threads.value()
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

    def mode_changed(self, mode):
        """
        Changes the mode on the parent
        """

        try:
            self.parent.mode = str(mode)
        except AttributeError:
            pass

    def set_defaults(self):

        """
        Set defaults back to what they were
        """

        self.gui.cmb_Mode.setCurrentIndex(2)
        self.gui.cmb_Quality.setCurrentIndex(2)
        self.gui.spin_Threads.setValue(5)

if __name__ == "__main__":

    APPLICATION = QtGui.QApplication(sys.argv)
    MAINWINDOW = OptionsDialog()
    MAINWINDOW.show()
    sys.exit(APPLICATION.exec_())