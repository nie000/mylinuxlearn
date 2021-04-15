import sys
from PySide import QtGui
from PySide.QtCore import QDir, QModelIndex
from PySide.QtGui import QTreeView, QFileSystemModel


class Explorer(QTreeView):
    def __init__(self, parent=None):
        QTreeView.__init__(self)
        self.header().setHidden(True)
        self.setAnimated(True)

        # Modelo
        self.model = QFileSystemModel(self)
        # path = QDir.toNativeSeparators(QDir.homePath())
        # self.model.setRootPath(path)
        self.setModel(self.model)

        # Se ocultan algunas columnas
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        # Conexion
        self.doubleClicked.connect(self._open_file)

    def _open_file(self, i):
        print(i)
        if not self.model.isDir(i):
            indice = self.model.index(i.row(), 0, i.parent())
            archivo = self.model.filePath(indice)
            print(archivo)


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