# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(313, 212)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 20, 61, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 61, 21))
        self.label_2.setObjectName("label_2")
        self.start_id = QtWidgets.QLineEdit(Form)
        self.start_id.setGeometry(QtCore.QRect(30, 40, 251, 20))
        self.start_id.setObjectName("start_id")
        self.start_pwd = QtWidgets.QLineEdit(Form)
        self.start_pwd.setGeometry(QtCore.QRect(30, 90, 251, 20))
        self.start_pwd.setObjectName("start_pwd")
        self.btn_startLogin = QtWidgets.QPushButton(Form)
        self.btn_startLogin.setGeometry(QtCore.QRect(30, 130, 251, 51))
        self.btn_startLogin.setObjectName("btn_startLogin")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "아이디"))
        self.label_2.setText(_translate("Form", "비밀번호"))
        self.btn_startLogin.setText(_translate("Form", "로그인"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
