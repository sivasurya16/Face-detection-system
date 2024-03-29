# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_Files\AboutUS.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(432, 421)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("UI_Files\\facial-recognition.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(True)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(150, 70, 141, 141))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("UI_Files\\facial-recognition.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(160, 230, 361, 51))
        self.label_3.setStyleSheet("font:14pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(40, 280, 131, 51))
        self.label_4.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";")
        self.label_4.setObjectName("label_4")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 230, 111, 51))
        self.label_2.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(150, 320, 131, 31))
        self.label_5.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(150, 350, 141, 31))
        self.label_6.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(150, 380, 111, 31))
        self.label_7.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(40, 20, 231, 41))
        self.label_8.setStyleSheet("font: 20pt \"MS Shell Dlg 2\";")
        self.label_8.setObjectName("label_8")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "About Us"))
        self.label_3.setText(_translate("Dialog", "FACE RECOGNITION 1.0(2022)"))
        self.label_4.setText(_translate("Dialog", "CREDITS:"))
        self.label_2.setText(_translate("Dialog", "VERSION:"))
        self.label_5.setText(_translate("Dialog", "SIVASURYA M"))
        self.label_6.setText(_translate("Dialog", "SAAMRAAJ R B"))
        self.label_7.setText(_translate("Dialog", "SRIHARI S"))
        self.label_8.setText(_translate("Dialog", "ABOUT US:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
