import sys
from PySide import QtGui

from PySide.QtCore import QDir
from PySide.QtGui import QTreeView

from QtLib.ChangeModel import FileSystemModel


class Explorer(QTreeView):
    def __init__(self, path,  parent=None):
        QTreeView.__init__(self)
        self.header().setHidden(True)
        self.setAnimated(True)
        # Modelo
        self.model = FileSystemModel()
        # path = QDir.toNativeSeparators(QDir.homePath())
        self.model.setRootPath(path)
        # self.setModel(self.model)
        # self.setRootIndex(QModelIndex(self.model.index(path)))
        # self.model.setNameFilters(["*.exe", "*.log", "*.s"])
        self.model.setNameFilterDisables(False)
        self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)

        # Se ocultan algunas columnas
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

        # Conexion
        self.doubleClicked.connect(self._open_file)

    def _open_file(self, i):
        if self.model.isDir(i):
            indice = self.model.index(i.row(), 0, i.parent())
            archivo = self.model.filePath(indice)
            print(archivo)

    def test(self, signal):
        file_path=self.model().filePath(signal)
        print(file_path)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    treeView = Explorer(path='C:/')
    treeView.show()
    app.exec_()