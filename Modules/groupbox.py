# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_Files\groupbox.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Details(object):
    def setupUi(self, Details):
        Details.setObjectName("Details")
        Details.resize(322, 232)
        font = QtGui.QFont()
        font.setPointSize(18)
        Details.setFont(font)
        Details.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        Details.setFlat(False)
        Details.setCheckable(False)
        self.gridLayoutWidget = QtWidgets.QWidget(Details)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 30, 321, 191))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.nameLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.nameLabel.setText("")
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout.addWidget(self.nameLabel, 0, 1, 1, 1)

        self.retranslateUi(Details)
        QtCore.QMetaObject.connectSlotsByName(Details)

    def retranslateUi(self, Details):
        _translate = QtCore.QCoreApplication.translate
        Details.setWindowTitle(_translate("Details", "GroupBox"))
        Details.setTitle(_translate("Details", "Details"))
        self.label.setText(_translate("Details", "Name"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Details = QtWidgets.QGroupBox()
    ui = Ui_Details()
    ui.setupUi(Details)
    Details.show()
    sys.exit(app.exec_())
