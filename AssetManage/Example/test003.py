# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/12 13:57
# @File     : test003.py
# @Software : PyCharm

import sys

from PySide.QtCore import Qt, QSize
from PySide.QtGui import QLabel, QFont, QPixmap, QHBoxLayout, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, \
    QApplication, QDialogButtonBox


class MyLable(QWidget):
    """ a widget contains a picture and two line of text """
    def __init__(self, title, subtitle, icon_path):
        """
        :param title: str title
        :param subtitle: str subtitle
        :param icon_path: path of picture
        """
        super(MyLable, self).__init__()
        self.lb_title = QLabel(title)
        self.lb_title.setFont(QFont("Arial", 10, QFont.Bold))
        self.lb_subtitle = QLabel(subtitle)
        self.lb_subtitle.setFont(QFont("Arial", 8, QFont.StyleItalic))

        self.lb_subtitle1 = QLabel(subtitle)
        self.lb_subtitle1.setFont(QFont("Arial", 8, QFont.StyleItalic))

        self.lb_icon = QLabel()
        self.lb_icon.setFixedSize(40, 40)
        pixMap = QPixmap(icon_path).scaled(self.lb_icon.width(), self.lb_icon.height())
        self.lb_icon.setPixmap(pixMap)

        self.lb_icon1 = QLabel()
        self.lb_icon1.setFixedSize(40, 40)
        pixMap1 = QPixmap(icon_path).scaled(self.lb_icon.width(), self.lb_icon.height())
        self.lb_icon1.setPixmap(pixMap1)

        self.double_click_fun = None
        self.init_ui()

    def init_ui(self):
        """handle layout"""
        ly_main = QHBoxLayout()
        ly_right = QVBoxLayout()
        ly_right.addWidget(self.lb_title)
        ly_right.addWidget(self.lb_subtitle)
        ly_right.addWidget(self.lb_subtitle1)
        ly_right.setAlignment(Qt.AlignVCenter)
        ly_main.addWidget(self.lb_icon)
        ly_main.addLayout(ly_right)
        ly_main.addWidget(self.lb_icon1)

        self.setLayout(ly_main)
        self.resize(90, 60)

    def get_lb_title(self):
        return self.lb_title.text()

    def get_lb_subtitle(self):
        return self.lb_subtitle.text()


class ListWindow(QWidget):
    def __init__(self, list_text, pic_path):
        super(ListWindow, self).__init__()
        self.doubleclick_fun = None
        self._set_items(list_text, pic_path)

    def _set_items(self, list_text, pic_path):
        """
        set the layout of listwidget
        :param list_text: list contains [title, subtitle]
        :param pic_path: string or list of strings
        """
        print list_text
        self.list_widget = QListWidget()
        ly_vbox = QVBoxLayout()
        if type(pic_path) is not list:
            for item in list_text:
                self._setItem(item[0], item[1], pic_path)
        else:
            for i in range(len(list_text)):
                self._setItem(list_text[i][0], list_text[i][1], pic_path[i])
        ly_vbox.addWidget(self.list_widget)
        self.list_widget.itemDoubleClicked.connect(self.item_doubleclick_slot)
        self.setLayout(ly_vbox)
        self.resize(300, 400)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |QDialogButtonBox.Cancel)
        ly_vbox.addWidget(buttonBox)
        buttonBox.accepted.connect(self.check_test)
        buttonBox.rejected.connect(self.reject)
        self.check_test()

    def check_test(self):
        pass

    def reject(self):
        print "XX"

    def _setItem(self, title, subtitle, pic_path):
        item_widget = QListWidgetItem()
        item_widget.setSizeHint(QSize(90, 60))
        self.list_widget.addItem(item_widget)

        label = MyLable(title, subtitle, pic_path)
        self.list_widget.setItemWidget(item_widget, label)

    def item_doubleclick_slot(self):
        if self.doubleclick_fun:
            widget = self.list_widget.itemWidget(self.list_widget.currentItem()) # get MyLabel widget
            self.doubleclick_fun(widget.get_lb_title(), widget.get_lb_subtitle())

    def set_doubleclick_slot(self, fun):
        """set item double click slot"""
        self.doubleclick_fun = fun


def diaplay(name, mac):
    print("title:", name, "Subtitle:", mac)


def main():
    list_out = []
    for i in range(5):
        list_item = []
        list_item.append("youtube")
        list_item.append("i like maria + " + str(i))
        list_item.append("i like marixxxxxa + " + str(i))
        list_out.append(list_item)

    pic_path = "../img/ToolWidget/tiJian.png"
    app = QApplication(sys.argv)
    mainwindow = ListWindow(list_out, pic_path)
    mainwindow.set_doubleclick_slot(diaplay)
    mainwindow.show()
    app.exec_()

if __name__ == '__main__':
    main()

