# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/16 9:29
# @File     : test007.py
# @Software : PyCharm

import sys
from PyQt4 import QtGui, QtCore


class OpenFile(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Open File')
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()
        self.setFocus()

        exit = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        exit.setShortcut('Ctrl+O')
        exit.setStatusTip('Open new File')
        self.connect(exit, QtCore.SIGNAL('triggered()'), self.showDialog)

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)

    def showDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', './')
        file = open(filename)
        data = file.read()
        self.textEdit.setText(data)


app = QtGui.QApplication(sys.argv)
of = OpenFile()
of.show()
sys.exit(app.exec_())