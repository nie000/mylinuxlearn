# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/19 15:23
# @File     : AssetsCreate.py
# @Software : PyCharm
import os
import shutil

from MayaLib import ControllerLibrary
from MayaLib.Maya import selected
from MayaLib.maya_import_export.maya_abc_export import maya_abc_export
from MayaLib.maya_import_export.maya_fbx_export import maya_fbx_export
from MayaLib.maya_import_export.maya_obj_export import maya_obj_export

from Qt import QtWidgets, QtCore
from QtLib.CheckBox import CheckBox
from QtLib.message import Message
from QtLib.screen_shot.screen_shot import ThumbnailWidget
from lib.CreateDir import mk_dir


class Path(object):
    path = ''

    def __init__(self):
        self.assets_name = ''
        self.filename = ''

    @property
    def assets_dir(self):
        return self.join(self.path, self.assets_name)

    @property
    def ma_path(self):
        return self.join(self.assets_dir, self.filename + '.ma')    \

    @property
    def json_path(self):
        return self.join(self.assets_dir, self.filename + '.json')

    @property
    def pic_path(self):
        return self.join(self.assets_dir, self.assets_name+'.png')

    @property
    def obj_path(self):
        return self.joins(self.assets_dir, 'obj', self.filename+'.obj')

    @property
    def abc_path(self):
        return self.joins(self.assets_dir, 'abc', self.filename+'.abc')

    @property
    def fbx_path(self):
        return self.joins(self.assets_dir, 'fbx', self.filename+'.fbx')

    def join(self, path1, path2):
        return os.path.join(path1, path2).replace('\\', '/')

    def joins(self, path1, path2, path3):
        return os.path.join(path1, path2, path3).replace('\\', '/')


class CreateAssetsUi(QtWidgets.QDialog, Path):

    def __init__(self):
        super(CreateAssetsUi, self).__init__()
        self.msg = Message()

        # self.screenshots_label = QtWidgets.QLabel(u'截图')
        self.screenshots_btn = ThumbnailWidget()
        self.name_label = QtWidgets.QLabel(u'Name')
        self.name_input = QtWidgets.QLineEdit(u"")
        self.file_name_label = QtWidgets.QLabel(u'fileName')
        self.file_name_input = QtWidgets.QLineEdit(u"")
        self.comment_label = QtWidgets.QLabel(u'Comment')
        self.comment_edit = QtWidgets.QTextEdit()

        self.box_export_ma =CheckBox(u'MaYa Export Ma')
        self.box_export_ma.toggle()
        self.box_export_ma.setTristate(False)
        self.box_export_ma.setCheckState(QtCore.Qt.PartiallyChecked)
        # self.box_export_mb = QtWidgets.QCheckBox(u'MaYa Export Mb', self)
        self.box_export_fbx = QtWidgets.QCheckBox(u'MaYa Export Fbx', self)
        self.box_export_abc = QtWidgets.QCheckBox(u'MaYa Export Abc', self)
        self.box_export_obj = QtWidgets.QCheckBox(u'MaYa Export obj', self)

        # self.box_export_proxy = QtWidgets.QCheckBox(u'MaYa Export proxy', self)
        self.create_btn = QtWidgets.QPushButton(u"create")
        self.create_btn.clicked.connect(self.create_assets)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.screenshots_btn, 1, 0, 2, 2)
        grid.addWidget(self.name_label, 3, 0)
        grid.addWidget(self.name_input,  3, 1)
        grid.addWidget(self.file_name_label, 4, 0)
        grid.addWidget(self.file_name_input,  4, 1)
        grid.addWidget(self.comment_label, 5, 0)
        grid.addWidget(self.comment_edit, 6, 0, 2, 2)

        grid.addWidget(self.box_export_ma, 9, 0)
        # grid.addWidget(self.box_export_mb, 9, 0)
        grid.addWidget(self.box_export_fbx, 10, 0)
        grid.addWidget(self.box_export_abc, 11, 0)
        grid.addWidget(self.box_export_obj, 12, 0)
        # grid.addWidget(self.box_export_proxy, 13, 0)
        grid.addWidget(self.create_btn, 14, 0, 1,3)

        self.setLayout(grid)
        self.setWindowTitle('grid layout')
        self.resize(200, 300)

    def create_assets(self):
        if self.check_input():
            get_create_info = {}
            screenshots = self.screenshots_btn.get_thumbnail_path()
            if screenshots:
                get_create_info.update({'screenshot': self.pic_path})
            coment = self.comment_edit.toPlainText()
            if self.is_checked():
                if selected():
                    create_info = self.get_create_info()
                    get_create_info.update(create_info)
                else:
                    return self.msg.warning(msg='please select a obj')
            get_create_info.update({'coment': coment, 'name': self.assets_name, 'path': self.ma_path, 'json_path': self.json_path})
            self.move_file(screenshots, self.pic_path)
            data = ControllerLibrary.ControllerLibrary()
            data.save(**get_create_info)

    def get_create_info(self):
        data_dict = {}
        if self.box_export_fbx.isChecked():
            fbx_path = os.path.dirname(self.fbx_path)
            maya_fbx_export(fbx_path, self.assets_name)
            data_dict['fbx'] = self.fbx_path
        if self.box_export_obj.isChecked():
            # obj_path =os.path.dirname(self.obj_path)
            maya_obj_export(self.obj_path)
            data_dict['obj'] = self.obj_path
        if self.box_export_abc.isChecked():
            abc_path = os.path.dirname(self.abc_path)
            maya_abc_export(abc_path, self.assets_name)
            data_dict['abc'] = self.abc_path
        return data_dict

    def is_checked(self):
        flag = 0
        if self.box_export_fbx.isChecked():
            flag = 1
        if self.box_export_obj.isChecked():
            flag = 1
        if self.box_export_abc.isChecked():
            flag = 1

        return flag

    def move_file(self, source_dir, target_dir):
        _dir = os.path.dirname(target_dir)
        if not os.path.exists(_dir):
            mk_dir(_dir)
        shutil.copy(source_dir, target_dir)

    def check_input(self):
        self.assets_name = self.name_input.text()
        self.filename = self.file_name_input.text()
        if not self.assets_name:
            self.msg.warning(msg='input your name')
            return
        if not self.filename:
            self.msg.warning(msg='input your filename')
            return
        if not self.path:
            self.msg.warning(msg='please select dir')
            return
        if not self.is_checked():
            if not self.screenshots_btn.get_thumbnail_path():
                self.msg.warning(msg='please screenshots')
                return
            else:
                pass
        return 1


