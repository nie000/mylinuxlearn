# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/23 8:42
# @File     : CheckBox.py
# @Software : PyCharm

from Qt import QtWidgets


class CheckBox(QtWidgets.QCheckBox):

    def __init__(self, parent=None):
        super(CheckBox, self).__init__(parent)

    def mousePressEvent(self, e):
        pass