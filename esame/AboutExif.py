# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AboutExif.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutExif(object):
    def setupUi(self, AboutExif):
        AboutExif.setObjectName("AboutExif")
        AboutExif.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(AboutExif)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(AboutExif)
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutExif)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(AboutExif)
        self.buttonBox.accepted.connect(AboutExif.accept)
        self.buttonBox.rejected.connect(AboutExif.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutExif)

    def retranslateUi(self, AboutExif):
        _translate = QtCore.QCoreApplication.translate
        AboutExif.setWindowTitle(_translate("AboutExif", "Dialog"))
        self.label.setText(_translate("AboutExif", "This is an Exif reader"))

