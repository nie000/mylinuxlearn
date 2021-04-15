# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/12 13:57
# @File     : AssetsSetRootDir.py
# @Software : PyCharm

import sys
from os.path import isdir

from Qt import QtWidgets, QtGui, QtCore
from QtLib.FileOpen import FileDialog
from QtLib.Qlable import Label
from config.SetConfig import ini
from lib import CreateDir

assets_dir = '/dir'


class MyLable(QtWidgets.QDialog):
    """ a widget contains a picture and two line of text """
    def __init__(self, item, icon_path):

        super(MyLable, self).__init__()
        self.lb_project_name = QtWidgets.QLabel(item['project_name'])
        self.lb_project_name.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
        self.lb_description = QtWidgets.QLabel(item['description'])
        self.lb_description.setFont(QtGui.QFont("Arial", 8, QtGui.QFont.StyleItalic))

        self.lb_project_path = QtWidgets.QLabel(item['project_path'])
        self.lb_project_path.setFont(QtGui.QFont("Arial", 8, QtGui.QFont.StyleItalic))

        self.lb_icon =QtWidgets. QLabel()
        self.lb_icon.setFixedSize(40, 40)
        pixMap = QtGui.QPixmap(item['project_picture_path']).scaled(self.lb_icon.width(), self.lb_icon.height())
        self.lb_icon.setPixmap(pixMap)

        self.lb_sel_path = Label(item['project_path'], item['root_dir'])
        self.lb_sel_path.setFixedSize(40, 40)
        pixMap1 =QtGui.QPixmap(icon_path).scaled(self.lb_icon.width(), self.lb_icon.height())
        self.lb_sel_path.setPixmap(pixMap1)
        self.lb_sel_path.click_signal.connect(self.set_dir_root)

        self.double_click_fun = None
        self.init_ui()

    def init_ui(self):
        """handle layout"""
        ly_main = QtWidgets.QHBoxLayout()
        ly_right = QtWidgets.QVBoxLayout()
        ly_right.addWidget(self.lb_project_name)
        ly_right.addWidget(self.lb_description)
        ly_right.addWidget(self.lb_project_path)
        ly_right.setAlignment(QtCore.Qt.AlignVCenter)
        ly_main.addWidget(self.lb_icon)
        ly_main.addLayout(ly_right)
        ly_main.addWidget(self.lb_sel_path)

        self.setLayout(ly_main)
        self.resize(90, 60)

    def get_lb_project_name(self):
        return self.lb_project_name.text()

    def get_lb_subtitle(self):
        return self.lb_description.text()

    def set_dir_root(self, list_data):
        dialog = FileDialog()
        if isdir(list_data[0]):
            get_sel_path = dialog.directory(start_path=list_data[0])
        else:
            get_sel_path = dialog.directory(start_path='C:/')
        if get_sel_path:
            self.lb_project_path.setText(get_sel_path)
            self.update_data(list_data[1], get_sel_path)

    def update_data(self, root_dir, update_dir):
        ini.update_data('RootDir', root_dir, update_dir)
        self.create_dir(update_dir)

    def create_dir(self, update_dir):
        CreateDir.mk_dir(update_dir+assets_dir)


class ListWindow(QtWidgets.QWidget):
    def __init__(self, ListViewData, open_picture_path):
        super(ListWindow, self).__init__()
        self.doubleclick_fun = None
        self._set_items(ListViewData, open_picture_path)
        self.setWindowTitle(u'设置根目录')

    def _set_items(self, list_data, file_open_picture):

        self.list_widget = QtWidgets.QListWidget()
        ly_vbox = QtWidgets.QVBoxLayout()

        for item in list_data:
            self._setItem(item, file_open_picture)

        ly_vbox.addWidget(self.list_widget)
        self.list_widget.itemDoubleClicked.connect(self.item_doubleclick_slot)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok |QtWidgets.QDialogButtonBox.Cancel)
        ly_vbox.addWidget(button_box)
        button_box.accepted.connect(self.close)
        button_box.rejected.connect(self.reject)

        self.setLayout(ly_vbox)
        self.resize(300, 400)
        self.check_test()

    def check_test(self):
        pass

    def reject(self):
        print "no write"

    def _setItem(self, item, file_open_picture):
        item_widget = QtWidgets.QListWidgetItem()
        item_widget.setSizeHint(QtCore.QSize(90, 60))
        self.list_widget.addItem(item_widget)

        label = MyLable(item, file_open_picture)
        self.list_widget.setItemWidget(item_widget, label)

    def item_doubleclick_slot(self):
        if self.doubleclick_fun:
            widget = self.list_widget.itemWidget(self.list_widget.currentItem())  # get MyLabel widget
            self.doubleclick_fun(widget.get_lb_project_name(), widget.get_lb_subtitle())

    def set_doubleclick_slot(self, fun):
        """set item double click slot"""
        self.doubleclick_fun = fun


def diaplay(name, mac):
    print("title:", name, "Subtitle:", mac)


def main():
    app = QApplication(sys.argv)
    mainwindow = ListWindow()
    mainwindow.set_doubleclick_slot(diaplay)
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()

