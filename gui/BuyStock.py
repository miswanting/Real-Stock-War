# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BuyStock.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BuyStock(object):
    def setupUi(self, BuyStock):
        BuyStock.setObjectName("BuyStock")
        BuyStock.resize(400, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(BuyStock.sizePolicy().hasHeightForWidth())
        BuyStock.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(BuyStock)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_stock_info = QtWidgets.QGroupBox(BuyStock)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_stock_info.sizePolicy().hasHeightForWidth())
        self.groupBox_stock_info.setSizePolicy(sizePolicy)
        self.groupBox_stock_info.setObjectName("groupBox_stock_info")
        self.gridLayout.addWidget(self.groupBox_stock_info, 0, 0, 2, 1)
        self.label_prefix = QtWidgets.QLabel(BuyStock)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_prefix.sizePolicy().hasHeightForWidth())
        self.label_prefix.setSizePolicy(sizePolicy)
        self.label_prefix.setObjectName("label_prefix")
        self.gridLayout.addWidget(self.label_prefix, 1, 1, 1, 1)
        self.spinBox_buy_amount = QtWidgets.QSpinBox(BuyStock)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_buy_amount.sizePolicy().hasHeightForWidth())
        self.spinBox_buy_amount.setSizePolicy(sizePolicy)
        self.spinBox_buy_amount.setObjectName("spinBox_buy_amount")
        self.gridLayout.addWidget(self.spinBox_buy_amount, 1, 2, 1, 1)
        self.label_fix = QtWidgets.QLabel(BuyStock)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_fix.sizePolicy().hasHeightForWidth())
        self.label_fix.setSizePolicy(sizePolicy)
        self.label_fix.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_fix.setObjectName("label_fix")
        self.gridLayout.addWidget(self.label_fix, 1, 3, 1, 1)
        self.pushButton_buy = QtWidgets.QPushButton(BuyStock)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_buy.sizePolicy().hasHeightForWidth())
        self.pushButton_buy.setSizePolicy(sizePolicy)
        self.pushButton_buy.setObjectName("pushButton_buy")
        self.gridLayout.addWidget(self.pushButton_buy, 2, 0, 1, 1)
        self.pushButton_cancel = QtWidgets.QPushButton(BuyStock)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_cancel.sizePolicy().hasHeightForWidth())
        self.pushButton_cancel.setSizePolicy(sizePolicy)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.gridLayout.addWidget(self.pushButton_cancel, 2, 1, 1, 3)
        self.groupBox_user_info = QtWidgets.QGroupBox(BuyStock)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_user_info.sizePolicy().hasHeightForWidth())
        self.groupBox_user_info.setSizePolicy(sizePolicy)
        self.groupBox_user_info.setObjectName("groupBox_user_info")
        self.gridLayout.addWidget(self.groupBox_user_info, 0, 1, 1, 3)

        self.retranslateUi(BuyStock)
        QtCore.QMetaObject.connectSlotsByName(BuyStock)

    def retranslateUi(self, BuyStock):
        _translate = QtCore.QCoreApplication.translate
        BuyStock.setWindowTitle(_translate("BuyStock", "Form"))
        self.groupBox_stock_info.setTitle(_translate("BuyStock", "股票信息"))
        self.label_prefix.setText(_translate("BuyStock", "买入："))
        self.label_fix.setText(_translate("BuyStock", "支"))
        self.pushButton_buy.setText(_translate("BuyStock", "买入"))
        self.pushButton_cancel.setText(_translate("BuyStock", "取消"))
        self.groupBox_user_info.setTitle(_translate("BuyStock", "账户信息"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BuyStock = QtWidgets.QWidget()
    ui = Ui_BuyStock()
    ui.setupUi(BuyStock)
    BuyStock.show()
    sys.exit(app.exec_())

