# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/11 15:40
# @File     : Splitter.py
# @Software : PyCharm
# -*- coding: utf-8 -*-
import os
import sys
from functools import partial

import AssetsCreate
import AssetsDir
from Qt import QtWidgets, QtCore, QtGui

from QtLib.ThumbListWidget import ThumbListWidget
from MayaLib.ControllerLibrary import ControllerLibrary
assets_dir = '/dir'


class FilePath(object):

    current_list_widget_path = ''

    def __init__(self):
        pass

    @property
    def ma_path(self):
        ma_path = ''
        if self.current_list_widget_path:
            ma_path = self.current_list_widget_path+'/ma/{}.ma'.format(self.name)
        return ma_path

    # @property
    # def pic_path(self):
    #     pass

    @property
    def name(self):
        return os.path.basename(self.current_list_widget_path)

    @property
    def pic_path(self):
        return self.current_list_widget_path + '/{}.png'.format(self.name)


class Splitter(QtWidgets.QWidget, FilePath):
    def __init__(self):
        super(Splitter, self).__init__()
        self.pic_size = 128
        hbox = QtWidgets.QHBoxLayout(self)
        self.setWindowTitle(u'QSplitter分割窗口')
        self.setGeometry(600, 600, 300, 200)
        self.splitter_left = AssetsDir.Explorer()
        self.splitter_left.clicked.connect(self.populate)
        self.splitter_left.clicked.connect(partial(self.change_stack, 0))

        self.splitter_center = ThumbListWidget(self)
        self.splitter_center.setViewMode(QtWidgets.QListWidget.IconMode)
        self.splitter_center.clicked.connect(partial(self.change_stack, 1))
        self.list_widget_conn()

        self.stack1 = AssetsCreate.CreateAssetsUi()
        # 创建资产菜单点击时刷新
        self.stack1.create_btn.clicked.connect(self.populate)

        # self.stack1.setMinimumWidth(100)

        self.stack2 = QtWidgets.QWidget()

        self.info_ui()

        self.Stack = QtWidgets.QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)

        splitter2 = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self)
        splitter2.addWidget(self.splitter_left)
        splitter2.setStretchFactor(0, 1)
        splitter2.addWidget(self.splitter_center)
        splitter2.setStretchFactor(1, 4)
        splitter2.addWidget(self.Stack)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)

    def info_ui(self):
        layout = QtWidgets.QFormLayout()
        self.Label1 = QtWidgets.QLabel()
        self.Label2 = QtWidgets.QLabel()
        self.Label3 = QtWidgets.QLabel()
        self.Label4 = QtWidgets.QLabel()
        layout.addRow(u"文件名", self.Label1)
        layout.addRow(u"文件地址", self.Label2)
        layout.addRow(u"图片地址", self.Label3)
        layout.addRow(u"评论", self.Label4)
        self.stack2.setLayout(layout)

    def change_stack(self, i, NotWhy):
        self.Stack.setCurrentIndex(i)
        if self.splitter_center.currentItem():
            self.current_list_widget_path = self.__current_list_widget_path()
            self.Label1.setText(self.name)
            self.Label2.setText(self.ma_path)
            self.Label3.setText(self.pic_path)
            self.Label4.setText('no write')

    def list_widget_conn(self):
        self.splitter_center.emit_filepath.connect(self.populate)
        self.splitter_center.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.splitter_center.customContextMenuRequested.connect(self.listItemRightClicked)
        self.splitter_center.itemDoubleClicked.connect(self.openImage)

    def populate(self):
        self.splitter_center.clear()
        try:
            path = self.__current_select_path()
        except:
            path = ''
        self.stack1.path = path
        data = ControllerLibrary()
        data.find(path)
        for name, info in data.items():
            self.list_widget_add_item(name, info['screenshot'])

    def listItemRightClicked(self, QPos):
        self.listMenu = QtWidgets.QMenu()
        open_folder_menu = self.listMenu.addAction(u"打开文件夹")
        replace_thumbnail_menu = self.listMenu.addAction(u"替换缩略图")
        add_comment_menu = self.listMenu.addAction(u"添加评论")
        bake_asset_menu = self.listMenu.addAction(u"备份资产")
        del_asset_menu = self.listMenu.addAction(u"删除资产")
        self.listMenu.addSeparator()
        ma_import_menu = self.listMenu.addAction(u"Maya Ma import")
        ma_open_menu = self.listMenu.addAction(u"Maya Ma open")
        abc_import_menu = self.listMenu.addAction(u"Maya Abc import")
        rs_import_menu = self.listMenu.addAction(u"Maya Rs import")
        rf_import_menu = self.listMenu.addAction(u"Maya Reference")

        parentPosition = self.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos+QtCore.QPoint(self.splitter_left.width(), 0))
        self.listMenu.show()

        open_folder_menu.triggered.connect(self.open_folder)

    def open_folder(self):
        os.startfile(self.__current_list_widget_path())

    def openImage(self):
        path = self.splitter_center.currentItem().toolTip()
        os.system(path)

    def open_ma_Folder(self):
        """
        鼠标右键操作 打开文件
        Returns:
        """

        file_path = self.__current_list_widget_path()
        filename = cmds.file(file_path, open=1, f=1, iv=1)

    def import_file(self):
        """
        import to maya
        Returns:

        """
        file_path = os.path.join(self.getdir, str(self.listWidget.currentItem().text()))
        pm.importFile(file_path)

    def import_reference(self):
        """
        导入reference
        :return:
        """
        filePath = os.path.join(self.getdir, str(self.listWidget.currentItem().text()))
        pm.createReference(filePath)

    def __current_select_path(self):
        index = self.splitter_left.currentIndex()
        model = index.model()
        dir = model.filePath(index)
        return dir.replace(assets_dir, '')

    def __current_list_widget_path(self):

        current_path = str(self.splitter_center.currentItem().toolTip())
        return os.path.dirname(current_path)

    def list_widget_add_item(self, name, screenshot):
        item = QtWidgets.QListWidgetItem(name)  # 添加QListWidget元素
        self.splitter_center.addItem(item)
        if screenshot:
            icon = QtGui.QIcon(screenshot)
            item.setIcon(icon)
            item.setToolTip(screenshot)
        self.splitter_center.setIconSize(QtCore.QSize(self.pic_size, self.pic_size))
        buffer = 12
        self.splitter_center.setGridSize(QtCore.QSize(self.pic_size + buffer, self.pic_size + buffer))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Splitter()
    demo.show()
    sys.exit(app.exec_())

