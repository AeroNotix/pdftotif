# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'options.ui'
#
# Created: Wed Dec 21 12:32:11 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(288, 145)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.spin_Threads = QtGui.QSpinBox(Dialog)
        self.spin_Threads.setMaximum(15)
        self.spin_Threads.setObjectName(_fromUtf8("spin_Threads"))
        self.gridLayout.addWidget(self.spin_Threads, 0, 1, 1, 1)
        self.cmb_Quality = QtGui.QComboBox(Dialog)
        self.cmb_Quality.setObjectName(_fromUtf8("cmb_Quality"))
        self.cmb_Quality.addItem(_fromUtf8(""))
        self.cmb_Quality.addItem(_fromUtf8(""))
        self.cmb_Quality.addItem(_fromUtf8(""))
        self.cmb_Quality.addItem(_fromUtf8(""))
        self.cmb_Quality.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmb_Quality, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.cmb_Mode = QtGui.QComboBox(Dialog)
        self.cmb_Mode.setObjectName(_fromUtf8("cmb_Mode"))
        self.cmb_Mode.addItem(_fromUtf8(""))
        self.cmb_Mode.addItem(_fromUtf8(""))
        self.cmb_Mode.addItem(_fromUtf8(""))
        self.cmb_Mode.addItem(_fromUtf8(""))
        self.cmb_Mode.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmb_Mode, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 1)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 5, 0, 1, 1)
        self.label.setBuddy(self.spin_Threads)
        self.label_2.setBuddy(self.cmb_Quality)

        self.retranslateUi(Dialog)
        self.cmb_Quality.setCurrentIndex(2)
        self.cmb_Mode.setCurrentIndex(2)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.cmb_Quality, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), Dialog.quality_change)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.set_defaults)
        QtCore.QObject.connect(self.cmb_Mode, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), Dialog.mode_changed)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Number of threads", None, QtGui.QApplication.UnicodeUTF8))
        self.cmb_Quality.setItemText(0, QtGui.QApplication.translate("Dialog", "Very Low Quality", None, QtGui.QApplication.UnicodeUTF8))
        self.cmb_Quality.setItemText(1, QtGui.QApplication.translate("Dialog", "Low Quality", None, QtGui.QApplication.UnicodeUTF8))
        self.cmb_Quality.setItemText(2, QtGui.QApplication.translate("Dialog", "Medium Quality", None, QtGui.QApplication.UnicodeUTF8))
        self.cmb_Quality.setItemText(3, QtGui.QApplication.translate("Dialog", "High Quality", None, QtGui.QApplication.UnicodeUTF8))
        self.cmb_Quality.setItemText(4, QtGui.QApplication.translate("Dialog", "Very High Quality", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Quality", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.cmb_Mode.setItemText(0, QtGui.QApplication.translate("Dialog", "tiffcrle", None, QtGui.QApplication.UnicodeUTF8))
        self.cmb_Mode.setItemText(1, QtGui.QApplication.translate("Dialog", "tiffg3", None, QtGui.QApplication.UnicodeUTF8))
        self.cmb_Mode.setItemText(2, QtGui.QApplication.translate("Dialog", "tiffg4", None, QtGui.QApplication.UnicodeUTF8))
        self.cmb_Mode.setItemText(3, QtGui.QApplication.translate("Dialog", "tifflzw", None, QtGui.QApplication.UnicodeUTF8))
        self.cmb_Mode.setItemText(4, QtGui.QApplication.translate("Dialog", "tiffpack", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Defaults", None, QtGui.QApplication.UnicodeUTF8))

