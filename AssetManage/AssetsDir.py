# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/12 13:57
# @File     : AssetsSetRootDir.py
# @Software : PyCharm
import os
import sys

from Qt import QtWidgets, QtCore, QtGui
from QtLib.ChangeModel import FileSystemModel
from QtLib.message import Message
from lib import CreateDir


class Explorer(QtWidgets.QTreeView):
    new_path = ''

    def __init__(self, parent=None):
        QtWidgets.QTreeView.__init__(self)
        self.header().setHidden(True)
        self.setAnimated(True)
        self.resize(70, 100)

        # Modelo
        self.model = FileSystemModel()
        self.setModel(self.model)
        self.model.setNameFilterDisables(False)
        self.model.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)
        self.model.setRootPath('')

        # Se ocultan algunas columnas
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

        # Conexion
        self.doubleClicked.connect(self._open_file)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.listItemRightClicked)

    def listItemRightClicked(self, QPos):
        self.listMenu = QtWidgets.QMenu()
        open_folder_menu = self.listMenu.addAction(u"打开文件夹")
        create_folder_menu = self.listMenu.addAction(u"创建文件夹")
        del_folder_menu = self.listMenu.addAction(u"删除文件夹")

        parentPosition = self.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()

        open_folder_menu.triggered.connect(self.open_folder)
        create_folder_menu.triggered.connect(self.create_folder)
        del_folder_menu.triggered.connect(self.del_folder)
        self.index_at = self.indexAt(QPos)

    def open_folder(self):

        os.startfile(self.__current_select_path())

    def create_folder(self):
        text = Message().input_dialog(title=u'创建文件夹', name=u'文件夹', default_name='')
        if text:
            all_path = self.join_path(self.__current_select_path(), text)
            CreateDir.mk_dir(all_path)

    def del_folder(self):
        print "no write"

    def __current_select_path(self):
        if not self.index_at.isValid():
            # 空白处点击
            path = self.new_path
        else:
            # 非空白点击
            index = self.currentIndex()
            model = index.model()
            path = model.filePath(index)
        return path

    def _open_file(self, i):
        if self.model.isDir(i):
            indice = self.model.index(i.row(), 0, i.parent())
            archivo = self.model.filePath(indice)

    def join_path(self, start_path, end_path):
        return os.path.join(start_path, end_path)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    treeView = Explorer()
    fileSystemModel = QtGui.QFileSystemModel(treeView)
    fileSystemModel.setReadOnly(False)
    root = fileSystemModel.setRootPath('C:/')
    fileSystemModel.setNameFilters(["*.exe", "*.log", "*.s"])
    fileSystemModel.setNameFilterDisables(False)
    treeView.setModel(fileSystemModel)
    treeView.setRootIndex(root)
    treeView.show()
    app.exec_()