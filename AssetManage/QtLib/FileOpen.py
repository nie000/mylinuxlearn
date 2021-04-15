# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/15 13:49
# @File     : FileOpen.py
# @Software : PyCharm
from Qt import QtWidgets


class FileDialog(QtWidgets.QDialog):

    def __init__(self):
        super(FileDialog, self).__init__()

    def directory(self, start_path='C:/'):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                     u"选取文件夹",
                                                     start_path)  # 起始路径
        return directory

    def openfilename(self):
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self,
                                                         u"选取文件",
                                                         "./",
                                                         "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        return filename, filetype

    def openfilenames(self):
        files, ok = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                 u"多文件选择",
                                                 "./",
                                                 "All Files (*);;Text Files (*.txt)")
        return files, ok

    def savefilename(self):
        filename, ok = QtWidgets.QFileDialog.getSaveFileName(self,
                                                   u"文件保存",
                                                   "./",
                                                   "All Files (*);;Text Files (*.txt)")
        return filename, ok


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myshow = FileDialog()
    myshow.show()
    sys.exit(app.exec_())
