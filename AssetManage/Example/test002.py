# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/12 10:11
# @File     : test002.py
# @Software : PyCharm
import sys
from PySide.QtCore import Qt
from PySide.QtGui import QMainWindow, QFont, QApplication, QSplitter, QTextEdit


class SplitterWidget(QMainWindow):
    def __init__(self, parent=None):
        super(SplitterWidget, self).__init__(parent)
        self.setWindowTitle("Splitter")

        font = QFont(self.tr("黑体"), 12)
        QApplication.setFont(font)

        mainSplitter = QSplitter(Qt.Horizontal, self)

        leftText = QTextEdit(self.tr("左窗口"), mainSplitter)
        leftText.setAlignment(Qt.AlignCenter)

        rightSplitter = QSplitter(Qt.Vertical, mainSplitter)
        rightSplitter.setOpaqueResize(False)

        upText = QTextEdit(self.tr("上窗口"), rightSplitter)
        upText.setAlignment(Qt.AlignCenter)

        bottomText = QTextEdit(self.tr("下窗口"), rightSplitter)
        bottomText.setAlignment(Qt.AlignCenter)

        mainSplitter.setStretchFactor(1, 1)
        mainSplitter.setWindowTitle(self.tr("分割窗口"))

        self.setCentralWidget(mainSplitter)


def main():
    app = QApplication(sys.argv)
    splitterWidget = SplitterWidget()
    splitterWidget.show()
    app.exec_()


main()