# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\how_pollute.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_How_Pollute(object):
    def setupUi(self, How_Pollute):
        How_Pollute.setObjectName("How_Pollute")
        How_Pollute.resize(1024, 538)
        self.background = QtWidgets.QLabel(How_Pollute)
        self.background.setGeometry(QtCore.QRect(0, 0, 1024, 540))
        self.background.setText("")
        self.background.setScaledContents(True)
        self.background.setObjectName("background")
        self.pushButton_previous = QtWidgets.QPushButton(How_Pollute)
        self.pushButton_previous.setGeometry(QtCore.QRect(50, 450, 300, 71))
        font = QtGui.QFont()
        font.setFamily("Cooper Black")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_previous.setFont(font)
        self.pushButton_previous.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_previous.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_previous.setAutoDefault(False)
        self.pushButton_previous.setObjectName("pushButton_previous")
        self.pushButton_next = QtWidgets.QPushButton(How_Pollute)
        self.pushButton_next.setGeometry(QtCore.QRect(674, 450, 300, 71))
        font = QtGui.QFont()
        font.setFamily("Cooper Black")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_next.setFont(font)
        self.pushButton_next.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_next.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_next.setAutoDefault(False)
        self.pushButton_next.setObjectName("pushButton_next")
        self.pushButton_back = QtWidgets.QPushButton(How_Pollute)
        self.pushButton_back.setGeometry(QtCore.QRect(10, 10, 281, 71))
        font = QtGui.QFont()
        font.setFamily("Cooper Black")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_back.setFont(font)
        self.pushButton_back.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_back.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_back.setAutoDefault(False)
        self.pushButton_back.setObjectName("pushButton_back")
        self.archie = QtWidgets.QLabel(How_Pollute)
        self.archie.setGeometry(QtCore.QRect(30, 90, 350, 350))
        self.archie.setText("")
        self.archie.setScaledContents(False)
        self.archie.setObjectName("archie")
        self.label_explanation = QtWidgets.QLabel(How_Pollute)
        self.label_explanation.setGeometry(QtCore.QRect(410, 20, 561, 391))
        font = QtGui.QFont()
        font.setFamily("Cooper Black")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.label_explanation.setFont(font)
        self.label_explanation.setLineWidth(-3)
        self.label_explanation.setScaledContents(False)
        self.label_explanation.setAlignment(QtCore.Qt.AlignCenter)
        self.label_explanation.setWordWrap(True)
        self.label_explanation.setObjectName("label_explanation")

        self.retranslateUi(How_Pollute)
        QtCore.QMetaObject.connectSlotsByName(How_Pollute)

    def retranslateUi(self, How_Pollute):
        _translate = QtCore.QCoreApplication.translate
        How_Pollute.setWindowTitle(_translate("How_Pollute", "Form"))
        self.pushButton_previous.setText(_translate("How_Pollute", "Previous"))
        self.pushButton_next.setText(_translate("How_Pollute", "Next"))
        self.pushButton_back.setText(_translate("How_Pollute", "BACK"))
        self.label_explanation.setText(_translate("How_Pollute", "What are we going to learn about??"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    How_Pollute = QtWidgets.QWidget()
    ui = Ui_How_Pollute()
    ui.setupUi(How_Pollute)
    How_Pollute.show()
    sys.exit(app.exec_())
