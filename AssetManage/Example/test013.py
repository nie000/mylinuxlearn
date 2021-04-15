# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/17 13:25
# @File     : test013.py
# @Software : PyCharm


from PySide import QtGui
from PySide import QtCore

import sys, os


class TreeView(QtGui.QTreeView):
    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)

        self.__model = QtGui.QFileSystemModel()
        self.__model.setRootPath(QtCore.QDir.rootPath())
        self.setModel(self.__model)

        self.__current_select_path = None
        self.doubleClicked.connect(self.__getCurPathEvent)

    # 双击信号 获得当前选中的节点的路径
    def __getCurPathEvent(self):
        index = self.currentIndex()
        model = index.model()  # 请注意这里可以获得model的对象
        self.__current_select_path = model.filePath(index)

    # 设置TreeView的跟文件夹
    def setPath(self, path):
        self.setRootIndex(self.__model.index(path))

    # 获得当前选中的节点的路径
    def getCurPath(self):
        return self.__current_select_path

# if __name__ == '__main__':
app = QtGui.QApplication(sys.argv)

asset = TreeView()
asset.setPath(r"D:")
asset.show()

sys.exit(app.exec_())
