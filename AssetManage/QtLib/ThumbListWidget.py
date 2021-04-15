# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/12 11:06
# @File     : slist.py
# @Software : PyCharm


from Qt import QtWidgets, QtCore, QtGui


class ThumbListWidget(QtWidgets.QListWidget):
    addfile = QtCore.Signal(str)
    emit_filepath = QtCore.Signal(str)
    dropped = QtCore.Signal(int, int)
    _rows_to_del = []
    wheel_value = 128

    def __init__(self, type, parent=None):
        super(ThumbListWidget, self).__init__(parent)
        self.setIconSize(QtCore.QSize(124, 124))
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.dropAction = QtCore.Qt.CopyAction
        self._dropping = False
        self.setSelectionRectVisible(True)
        self.dropped.connect(self.items_dropped)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.mimeData().urls()
            event.accept()
        else:
            super(ThumbListWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            super(ThumbListWidget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        filepath = ''
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                filepath = url.toLocalFile()
        self.emit_filepath.emit(filepath)

    def setCopyAction(self):
        print
        'copy'

    def setMoveAction(self):
        print
        'move'

    def rowsInserted(self, parent, start, end):
        if self._dropping:
            self.dropped.emit(start, end)
        super(ThumbListWidget, self).rowsInserted(parent, start, end)

    def dataChanged(self, start, end, *args, **kwargs):
        if self._dropping:
            for row in range(start.row(), end.row() + 1):
                index = self.indexFromItem(self.item(row))
                shot = index.data()
                self.addfile.emit(shot)
                if len(self.findItems(shot, QtCore.Qt.MatchExactly)) > 1:
                    self._rows_to_del.append(row)
            self._rows_to_del = []

    def items_dropped(self, start, end):
        for row in range(start, end + 1):
            item = self.item(row)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            if self.selectedItems():
                new_state = QtCore.Qt.Unchecked if self.selectedItems()[0].checkState() else QtCore.Qt.Checked
                for item in self.selectedItems():
                    if item.flags() & QtCore.Qt.ItemIsUserCheckable:
                        item.setCheckState(new_state)
            self.reset()
        elif event.key() == QtCore.Qt.Key_Delete:
            for item in self.selectedItems():
                self.takeItem(self.row(item))

    def new(self):
        """Unfinnished"""
        print
        'list widget 001'

    def cut(self):
        """Cut a node"""
        self.cutIndex = self.currentIndex()
        self.copyIndex = None

    def copy(self):
        """Copy a node"""
        self.cutIndex = None
        self.copyIndex = self.currentIndex()

    def paste(self):
        """Paste a node
        A node is pasted before the selected destination node
        """

        sourceIndex = None
        if self.cutIndex != None:
            sourceIndex = self.cutIndex
        elif self.copyIndex != None:
            sourceIndex = self.copyIndex

        if sourceIndex != None:
            destinationIndex = self.currentIndex()
            destinationItem = destinationIndex.internalPointer()
            destinationParentIndex = self.myModel.parent(index=destinationIndex)
            sourceItem = sourceIndex.internalPointer()
            sourceRow = sourceItem.row()
            sourceParentIndex = self.myModel.parent(index=sourceIndex)
            row = destinationItem.row()
            if self.cutIndex != None:
                self.myModel.moveItem(sourceParentIndex=sourceParentIndex,
                                      sourceRow=sourceRow,
                                      destinationParentIndex=destinationParentIndex,
                                      destinationRow=row)
            else:
                self.myModel.copyItem(sourceParentIndex=sourceParentIndex,
                                      sourceRow=sourceRow,
                                      destinationParentIndex=destinationParentIndex,
                                      destinationRow=row)

    def deleteItem(self):
        """Deletes the current item (node)"""
        currentIndex = self.currentIndex()
        currentItem = currentIndex.internalPointer()
        quitMessage = "Are you sure that %s should be deleted?" % currentItem.displayData
        messageBox = QtGui.QMessageBox(parent=self)
        reply = messageBox.question(self, 'Message',
                                    quitMessage, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            # This item is this row at its parents child list:
            row = currentItem.row()
            parentIndex = self.myModel.parent(index=currentIndex)
            self.myModel.removeRow(row=row, parentIndex=parentIndex)

    def wheelEvent(self, event):

        if event.delta() > 0:
            if self.wheel_value <= 400:
                self.wheel_value = self.wheel_value + 10
        else:
            if self.wheel_value > 80:
                self.wheel_value = self.wheel_value - 10
        self.setIconSize(QtCore.QSize(self.wheel_value, self.wheel_value))
        buffer = 12
        self.setGridSize(QtCore.QSize(self.wheel_value + buffer, self.wheel_value + buffer))

