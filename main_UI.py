# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Thu Nov 24 11:38:06 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(438, 232)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tab)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_4.addWidget(self.label_5, 0, 0, 1, 1)
        self.lineEdit_3 = QtGui.QLineEdit(self.tab)
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.gridLayout_4.addWidget(self.lineEdit_3, 0, 1, 1, 1)
        self.btn_single_file = QtGui.QToolButton(self.tab)
        self.btn_single_file.setObjectName(_fromUtf8("btn_single_file"))
        self.gridLayout_4.addWidget(self.btn_single_file, 0, 2, 1, 1)
        self.lineEdit_4 = QtGui.QLineEdit(self.tab)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.gridLayout_4.addWidget(self.lineEdit_4, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_4.addWidget(self.label_3, 1, 0, 1, 1)
        self.bt_output_single = QtGui.QToolButton(self.tab)
        self.bt_output_single.setObjectName(_fromUtf8("bt_output_single"))
        self.gridLayout_4.addWidget(self.bt_output_single, 1, 2, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.tab_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.tab_2)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.btn_dir_lookup = QtGui.QToolButton(self.tab_2)
        self.btn_dir_lookup.setObjectName(_fromUtf8("btn_dir_lookup"))
        self.gridLayout_2.addWidget(self.btn_dir_lookup, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.tab_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.btn_output_dir = QtGui.QToolButton(self.tab_2)
        self.btn_output_dir.setObjectName(_fromUtf8("btn_output_dir"))
        self.gridLayout_2.addWidget(self.btn_output_dir, 1, 2, 1, 1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 438, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.label_5.setBuddy(self.lineEdit)
        self.label.setBuddy(self.lineEdit)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.btn_single_file, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.single_locate_file)
        QtCore.QObject.connect(self.bt_output_single, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.single_output_file)
        QtCore.QObject.connect(self.btn_dir_lookup, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.dir_locate)
        QtCore.QObject.connect(self.btn_output_dir, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.dir_output)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.lineEdit, self.btn_dir_lookup)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_single_file.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Output Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.bt_output_single.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Single PDF Conversion", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_dir_lookup.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Output Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_output_dir.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Directory Conversion", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit..", None, QtGui.QApplication.UnicodeUTF8))

