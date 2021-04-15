# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/15 8:15
# @File     : test001.py
# @Software : PyCharm
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('../config/project.ini')

db_host = config.get('RootDir', 'ma_root_dir')
print(db_host)
