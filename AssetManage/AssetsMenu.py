# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/12 13:57
# @File     : AssetsSetRootDir.py
# @Software : PyCharm

from Qt import QtWidgets

from QtLib.Tool_Button import ToolButton
from config.SetConfig import list_view_data, ini


class LeftTitleWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LeftTitleWidget, self).__init__(parent)

        self.button_list = []

        # 版本标题颜色设置
        self.version_title = QtWidgets.QLabel()
        self.version_title.setStyleSheet("color:red")
        # for i in ListViewData:

        string_list = list_view_data(ini.get_data('RootDir', 'ma_root_dir'),
                                     ini.get_data('RootDir', 'tex_root_dir'),
                                     ini.get_data('RootDir', 'hdr_root_dir')
                                    )
        button_layout = QtWidgets.QVBoxLayout()
        for i in string_list:
            self.tool_button = ToolButton(i['project_picture_path'])
            self.button_list.append(self.tool_button)
            button_layout.addWidget(self.tool_button, 0)

        button_layout.addStretch()
        button_layout.setContentsMargins(0, 0, 0, 0)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(70)
        self.setLayout(main_layout)
        self.is_move = False

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    title = LeftTitleWidget()
    title.show()
    app.exec_()


