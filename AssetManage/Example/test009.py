# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/16 14:36
# @File     : test009.py
# @Software : PyCharm
from PyQt5.QtWidgets import QTreeView,QFileSystemModel,QApplication


class Main(QTreeView):
    def __init__(self):
        QTreeView.__init__(self)
        model = QFileSystemModel()
        model.setRootPath('C:\\')
        self.setModel(model)
        self.doubleClicked.connect(self.test)

    def test(self, signal):
        file_path=self.model().filePath(signal)
        print(file_path)


import sys
app = QApplication(sys.argv)
w = Main()
w.show()
sys.exit(app.exec_())