# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/16 15:05
# @File     : test011.py
# @Software : PyCharm
from __future__ import absolute_import

from PyQt4 import QtGui

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QTreeView
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QFileSystemModel
from PyQt4.QtGui import QHeaderView
from PyQt4.QtCore import QDir
from PyQt4.QtCore import SIGNAL

# from ninja_ide import translations


class AddToProject(QDialog):
    """Dialog to let the user choose one of the folders from the opened proj"""

    def __init__(self, projects, parent=None):
        super(AddToProject, self).__init__(parent)
        # pathProjects must be a list
        self._projects = projects
        self.setWindowTitle("XX")
        self.pathSelected = ''
        vbox = QVBoxLayout(self)

        hbox = QHBoxLayout()
        self._list = QListWidget()
        for project in self._projects:
            self._list.addItem(project['name'])

        # self._list.setCurrentRow(0)
        self._tree = QTreeView()
        # self._tree.header().setHidden(True)
        # self._tree.setSelectionMode(QTreeView.SingleSelection)
        # self._tree.setAnimated(True)
        self.load_tree(self._projects[0])
        hbox.addWidget(self._list)
        hbox.addWidget(self._tree)
        vbox.addLayout(hbox)

        hbox2 = QHBoxLayout()
        btnAdd = QPushButton("XX")
        btnCancel = QPushButton("XX")
        hbox2.addWidget(btnCancel)
        hbox2.addWidget(btnAdd)
        vbox.addLayout(hbox2)

        self.connect(btnCancel, SIGNAL("clicked()"), self.close)
        self.connect(btnAdd, SIGNAL("clicked()"), self._select_path)
        self.connect(self._list,
                     SIGNAL("currentItemChanged(QTreeWidgetItem*, QTreeWidgetItem*)"),
                     self._project_changed)

    def _project_changed(self, item, previous):
        # FIXME, this is not being called, at least in osx
        for each_project in self._projects:
            if each_project.name == item.text():
                self.load_tree(each_project)

    def load_tree(self, project):
        """Load the tree view on the right based on the project selected."""
        qfsm = QFileSystemModel()
        qfsm.setRootPath(project['path'])
        load_index = qfsm.index(qfsm.rootPath())
        # qfsm.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
        # qfsm.setNameFilterDisables(False)
        # pext = ["*{0}".format(x) for x in project['extensions']]
        # qfsm.setNameFilters(pext)

        self._tree.setModel(qfsm)
        self._tree.setRootIndex(load_index)

        t_header = self._tree.header()
        # t_header.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        # t_header.setResizeMode(0, QHeaderView.Stretch)
        # t_header.setStretchLastSection(False)
        # t_header.setClickable(True)
        #












        # self._tree.hideColumn(1)  # Size
        # self._tree.hideColumn(2)  # Type
        # self._tree.hideColumn(3)  # Modification date

        # FIXME: Changing the name column's title requires some magic
        # Please look at the project tree

    def _select_path(self):
        """Set pathSelected to the folder selected in the tree."""
        path = self._tree.model().filePath(self._tree.currentIndex())
        if path:
            self.pathSelected = path
            self.close()

import sys
app = QtGui.QApplication(sys.argv)
w = AddToProject(projects=[{'name': 'XX', 'path': 'C:/','extensions': "xx1"}])
w.show()
sys.exit(app.exec_())