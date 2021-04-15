# -*- coding: utf-8 -*-
import os
import maya.cmds as mc


def maya_obj_export(path, start=1, end=1, padding=4):
    print path, 123659
    parent_dir = os.path.dirname(path)
    if not os.path.isdir(parent_dir):
        os.makedirs(parent_dir)
    for i in range(start, end+1):
        mc.currentTime(i)
        prefix, suffix = os.path.splitext(path)
        new_path = "%s.%s%s" % (prefix, str(i).zfill(padding), suffix)
        mc.file(new_path, typ="OBJexport", options="groups=1; ptgroups=1;materials=1;smoothing=1;normals=1", pr=1, es=1)
