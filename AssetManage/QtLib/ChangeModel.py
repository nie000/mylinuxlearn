# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/16 16:02
# @File     : ChangeModel.py
# @Software : PyCharm
from Qt import QtWidgets


class FileSystemModel(QtWidgets.QFileSystemModel):

    def __init__(self):
        super(FileSystemModel, self).__init__()