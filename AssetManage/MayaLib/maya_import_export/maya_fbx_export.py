# -*- coding: utf-8 -*-
import os
import maya.mel as mel


def maya_fbx_export(file_dir, file_name):
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    mel.eval('file -force -options "v=0;" -typ "FBX export" -pr -es "%s/%s.fbx";' % (file_dir, file_name))
