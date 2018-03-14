# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QCaesarTemplate.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(901, 1286)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.diffView = PlotWidget(self.centralwidget)
        self.diffView.setGeometry(QtCore.QRect(50, 850, 800, 200))
        self.diffView.setObjectName(_fromUtf8("diffView"))
        self.dtmView = GLViewWidget(self.centralwidget)
        self.dtmView.setGeometry(QtCore.QRect(50, 30, 800, 800))
        self.dtmView.setObjectName(_fromUtf8("dtmView"))
        self.frameNumber = QtGui.QLCDNumber(self.centralwidget)
        self.frameNumber.setGeometry(QtCore.QRect(730, 1130, 111, 51))
        self.frameNumber.setObjectName(_fromUtf8("frameNumber"))
        self.horizontalSlider = QtGui.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(60, 1070, 791, 29))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(530, 1130, 175, 42))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(290, 1130, 181, 37))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 901, 40))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "Play Movie", None))
        self.checkBox.setText(_translate("MainWindow", "Play Movie", None))

from pyqtgraph import PlotWidget
from pyqtgraph.opengl import GLViewWidget
