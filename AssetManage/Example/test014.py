# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/18 15:10
# @File     : test014.py
# @Software : PyCharm
import sys
from PySide import QtGui, QtCore


class Escape(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)

        self.setWindowTitle(u'重写')
        self.resize(350, 250)
        self.connect(self, QtCore.SIGNAL('closeEmitAPP()'), QtCore.SLOT('close()'))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


app = QtGui.QApplication(sys.argv)
qb = Escape()
qb.show()