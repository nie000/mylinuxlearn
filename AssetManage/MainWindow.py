# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/10 15:39
# @File     : MainWindow.py
# @Software : PyCharm
import logging
from functools import partial

import AssetsMenu
import Splitter
from AssetsSetRootDir import diaplay, ListWindow
from Qt import QtWidgets, QtGui, QtCore
from config.SetConfig import open_picture_path, list_view_data, ini

logging.basicConfig()
logger = logging.getLogger('lightingManager')
logger.setLevel(logging.DEBUG)

import Qt

if Qt.__binding__ == 'PySide':
    logger.debug('Using PySide with shiboken')
    from shiboken import wrapInstance
elif Qt.__binding__.startswith('PyQt'):
    logger.debug('Using PyQt with sip')
else:
    logger.debug('Using PySide2 with shiboken2')
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui


def _get_maya_main_window():
    pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(long(pointer), QtWidgets.QWidget)

assets_dir = '/dir'


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self,  parent=None):
        super(MainWindow, self).__init__(_get_maya_main_window())
        self.resize(1250, 750)
        self.setWindowTitle(u'assets')
        assets_menu = AssetsMenu.LeftTitleWidget()
        self.splitter_window = Splitter.Splitter()
        assets_menu.button_list[0].clicked.connect(partial(self.change_dir, 'ma_root_dir'))
        assets_menu.button_list[1].clicked.connect(partial(self.change_dir, 'tex_root_dir'))
        assets_menu.button_list[2].clicked.connect(partial(self.change_dir, 'hdr_root_dir'))
        widget = QtWidgets.QWidget(self)
        HBox = QtWidgets.QHBoxLayout(widget)
        HBox.addWidget(assets_menu)
        HBox.addWidget(self.splitter_window)

        self.setCentralWidget(widget)

        help = QtWidgets.QAction(QtGui.QIcon('icons/help.png'), u'no write', self)
        help.setShortcut('Ctrl+Q')
        help.setStatusTip('help application')

        set_dir = QtWidgets.QAction(QtGui.QIcon('icons/help.png'), u'set root dir', self)
        set_dir.setShortcut('Ctrl+O')
        set_dir.setStatusTip('help application')
        set_dir.triggered.connect(self.root_dir_window)

        self.statusBar()
        menubar = self.menuBar()
        sets_menu = menubar.addMenu(u'&设置')
        help_menu = menubar.addMenu(u'&帮助')

        help_menu.addAction(help)
        sets_menu.addAction(set_dir)

    def root_dir_window(self):

        list_data = list_view_data(ini.get_data('RootDir', 'ma_root_dir'),
                                   ini.get_data('RootDir', 'tex_root_dir'),
                                   ini.get_data('RootDir', 'hdr_root_dir')
                            )

        self.path_window = ListWindow(list_data, open_picture_path)
        self.path_window.set_doubleclick_slot(diaplay)
        self.path_window.show()

    def change_dir(self, flag):
        path = ini.get_data('RootDir', flag)+assets_dir
        self.splitter_window.splitter_left.new_path = path
        self.splitter_window.splitter_left.model.setRootPath(path)
        self.splitter_window.splitter_left.setRootIndex(QtCore.QModelIndex(self.splitter_window.splitter_left.model.index(path)))


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    title = MainWindow()
    title.show()
    app.exec_()