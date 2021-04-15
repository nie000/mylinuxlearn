# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/16 14:33
# @File     : test008.py
# @Software : PyCharm

from PyQt4 import QtGui
from PyQt4 import QtCore


class Main(QtGui.QTreeView):

  def __init__(self):

    QtGui.QTreeView.__init__(self)
    model = QtGui.QFileSystemModel()
    model.setRootPath( QtCore.QDir.currentPath() )
    self.setModel(model)
    QtCore.QObject.connect(self.selectionModel(), QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'), self.test)

  @QtCore.pyqtSlot("QItemSelection, QItemSelection")
  def test(self, selected, deselected):
      print("hello!")
      print(selected)
      print(deselected)

import sys
app = QtGui.QApplication(sys.argv)
w = Main()
w.show()
sys.exit(app.exec_())