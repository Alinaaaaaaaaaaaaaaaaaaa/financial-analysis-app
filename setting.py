# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_setting(object):
    def setupUi(self, setting):
        setting.setObjectName("setting")
        setting.resize(734, 550)
        setting.setStyleSheet("background-color: #EC933B    ")
        self.label = QtWidgets.QLabel(setting)
        self.label.setGeometry(QtCore.QRect(270, 40, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #FFFFFF")
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(setting)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 460, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: #FFFFFF;\n"
"color: #5C2E00")
        self.pushButton_2.setObjectName("pushButton_2")
        self.comboBox = QtWidgets.QComboBox(setting)
        self.comboBox.setGeometry(QtCore.QRect(390, 180, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("color: #5C2E00")
        self.comboBox.setObjectName("comboBox")
        self.lineEdit = QtWidgets.QLineEdit(setting)
        self.lineEdit.setGeometry(QtCore.QRect(390, 280, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("color: #5C2E00")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_3 = QtWidgets.QPushButton(setting)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 460, 351, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color: #FFFFFF;\n"
"color: #5C2E00")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_6 = QtWidgets.QPushButton(setting)
        self.pushButton_6.setGeometry(QtCore.QRect(430, 220, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setStyleSheet("background-color: #FFFFFF;\n"
"color: #5C2E00")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(setting)
        self.pushButton_7.setGeometry(QtCore.QRect(430, 330, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setStyleSheet("background-color: #FFFFFF;\n"
"color: #5C2E00")
        self.pushButton_7.setObjectName("pushButton_7")
        self.label_2 = QtWidgets.QLabel(setting)
        self.label_2.setGeometry(QtCore.QRect(130, 170, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: #FFFFFF;\n"
"color: #5C2E00")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(setting)
        self.label_3.setGeometry(QtCore.QRect(120, 280, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color: #FFFFFF;\n"
"color: #5C2E00")
        self.label_3.setObjectName("label_3")

        self.retranslateUi(setting)
        QtCore.QMetaObject.connectSlotsByName(setting)

    def retranslateUi(self, setting):
        _translate = QtCore.QCoreApplication.translate
        setting.setWindowTitle(_translate("setting", "Financier"))
        self.label.setText(_translate("setting", "Настройки"))
        self.pushButton_2.setText(_translate("setting", " Меню"))
        self.pushButton_3.setText(_translate("setting", "Удалить последний внесенный платеж"))
        self.pushButton_6.setText(_translate("setting", "Удалить"))
        self.pushButton_7.setText(_translate("setting", "Сохранить"))
        self.label_2.setText(_translate("setting", "  Удалить сферу расходов:"))
        self.label_3.setText(_translate("setting", "  Добавить сферу расходов:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    setting = QtWidgets.QWidget()
    ui = Ui_setting()
    ui.setupUi(setting)
    setting.show()
    sys.exit(app.exec_())
