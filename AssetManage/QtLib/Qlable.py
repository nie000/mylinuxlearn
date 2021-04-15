# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/15 13:22
# @File     : Qlable.py
# @Software : PyCharm
from Qt import QtWidgets, QtCore


class Label(QtWidgets.QLabel):
    click_signal = QtCore.Signal(list)

    def __init__(self, project_path, root_dir, parent=None):
        super(Label, self).__init__(parent)
        self.project_path = project_path
        self.root_dir = root_dir

    # 重载一下鼠标点击事件
    def mousePressEvent(self, e):
        print "you clicked the label"
        list_data = [self.project_path, self.root_dir]
        self.click_signal.emit(list_data)

    # def mouseReleaseEvent(self, QMouseEvent):
    #     print 'you have release the mouse'
