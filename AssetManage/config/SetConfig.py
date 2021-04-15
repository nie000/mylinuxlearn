# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/14 13:55
# @File     : Config.py
# @Software : PyCharm
import os

import IniData

now_dir = os.path.dirname(os.path.realpath(__file__))

pic_path = os.path.dirname(now_dir)
ini = IniData.IniData(now_dir + '/project.ini')
# print ini.get_data('RootDir', 'ma_root_dir')


# ListViewData 可以存json
def list_view_data(ma_root_dir, tex_root_dir, hdr_root_dir):
    return [
                {'project_picture_path': pic_path+'/img/ToolWidget/ma.png', 'project_name': 'MaYa assets', 'project_path': ma_root_dir, 'description': u'保存ma文件根路径', 'root_dir': 'ma_root_dir'},
                {'project_picture_path': pic_path+'/img/ToolWidget/tex.png', 'project_name': 'MaYa TEX', 'project_path': tex_root_dir, 'description': u'保存材质根路径', 'root_dir': 'tex_root_dir'},
                {'project_picture_path': pic_path+'/img/ToolWidget/tiJian.png', 'project_name': 'MaYa HRD', 'project_path': hdr_root_dir, 'description': 'test', 'root_dir': 'hdr_root_dir'}
            ]

# 文件打开图片
open_picture_path = pic_path+"/img/ToolWidget/file_open.png"




