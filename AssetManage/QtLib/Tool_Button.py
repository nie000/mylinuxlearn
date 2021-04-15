# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/10 15:14
# @File     : tool_button0.py
# @Software : PyCharm

from Qt import QtWidgets, QtCore, QtGui


class ToolButton(QtWidgets.QToolButton):

    def __init__(self, pic_name, parent=None):
        super(ToolButton, self).__init__(parent)
        self.pixmap = QtGui.QPixmap(pic_name)
        self.setIcon( QtGui.QIcon(self.pixmap))
        self.setIconSize(self.pixmap.size())
        self.setFixedSize(self.pixmap.width() + 25, self.pixmap.height() + 27)
        self.setAutoRaise(True)

        self.text_palette = QtGui.QPalette()
        self.text_palette.setColor(self.text_palette.ButtonText,  QtGui.QColor(230, 230, 230))
        self.setPalette(self.text_palette)

        self.text_font = QtGui.QFont()
        self.text_font.setWeight(QtGui.QFont.Bold)

        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setStyleSheet("background:transparent")

        self.mouse_over = False
        self.mouse_press = False

    def enterEvent(self, event):
        self.mouse_over = True
        self.update()

    def leaveEvent(self, event):
        self.mouse_over = False
        self.update()

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.clicked.emit(True)

    def mouseDoubleClickEvent(self,e):
        print 'mouse double clicked'

    def setMousePress(self, mouse_press):
        self.mouse_press = mouse_press
        self.update()

    def paintEvent(self, event):
        if self.mouse_over:
            self.painterInfo(0, 100, 150)
        else:
            if self.mouse_press:
                self.painterInfo(0, 100, 150)
        QtWidgets.QToolButton.paintEvent(self, event)

    def painterInfo(self, top_color, middle_color, bottom_color):
        self.painter = QtGui.QPainter()
        self.painter.begin(self)
        self.painter.setPen(QtCore.Qt.NoPen)

        self.linear = QtGui.QLinearGradient(self.rect().topLeft(), self.rect().bottomLeft())
        self.linear.setColorAt(0, QtGui.QColor(230, 230, 230, top_color))
        self.linear.setColorAt(0.5, QtGui.QColor(230, 230, 230, middle_color))
        self.linear.setColorAt(1, QtGui.QColor(230, 230, 230, bottom_color))

        self.painter.setBrush(self.linear)
        self.painter.drawRect(self.rect())
        self.painter.end()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tool = ToolButton("./img/ToolWidget/gongNeng.png")
    # tool.setMousePress(True)
    tool.show()
    sys.exit(app.exec_())


