# -*- coding: utf-8 -*-
# @Time    : 2018/8/15 16:37
# @Author  : 聂家利
# @Email   : 1073438012@qq.com
# @File    : message.py
# @Software: PyCharm
from Qt import QtWidgets


class Message(QtWidgets.QDialog):

    def __init__(self):
        super(Message, self).__init__()

    def invalid_ok_cancel(self, msg=u'Invalid'):
        result = QtWidgets.QMessageBox.warning(
            self,
            "Invalid Attributes",
            msg,
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        )
        return result

    def warning(self, msg=u'不能这样做'):
        QtWidgets.QMessageBox.warning(self, "Warning", msg, QtWidgets.QMessageBox.Yes)

    def question(self, title=u'删除', question=u"确认删除吗"):
        reply = QtWidgets.QMessageBox.question(self, title, question, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        return 1 if reply == QtWidgets.QMessageBox.Yes else 0

    def input_dialog(self, title=u'删除', default_name='name', name="xx"):
        text, ok = QtWidgets.QInputDialog.getText(self, title, u'输入{}名称:'.format(name), text=default_name)
        return text if ok else 0

