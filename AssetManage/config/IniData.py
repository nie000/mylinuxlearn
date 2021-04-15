# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/12 16:26
# @File     : get_project_ini.py
# @Software : PyCharm

import ConfigParser


# 配置处理类
class IniData:
    __configdir = False

    def __init__(self, configdir=''):
        # 默认为空
        if not configdir.strip():
            self.__configdir = "./config/project.ini"
        else:
            self.__configdir = configdir
        return

    # 获取配置数据
    # string
    def get_data(self, section, option):
        config = ConfigParser.ConfigParser()
        try:
            config.read(self.__configdir)
            Ret = config.get(section, option)
            return Ret
        except Exception:
            return ""

    # 修改数据
    def update_data(self, section, option, value):
        config = ConfigParser.ConfigParser()
        try:
            config.read(self.__configdir)
            config.set(section, option, value)
            config.write(open(self.__configdir, "w"))
            return True
        except Exception:
            return False

    # 添加数据
    def add_data(self, section, option, value):
        config = ConfigParser.ConfigParser()
        try:
            config.read(self.__configdir)
            a = config.add_section(section)
            config.set(section, option, value)
            config.write(open(self.__configdir, "r+"))
            return True
        except Exception:
            return False


if __name__ == '__main__':
    t = IniData()
    print t.update_data("RootDir", "ma_root_dir", "12345")
    print t.get_data("RootDir", "ma_root_dir")