# -*- coding: utf-8 -*-
import re
import maya.cmds as mc
from MayaLib.maya_import_export.BaseHook import BaseHook
from MayaLib import Maya


class Hook(BaseHook):
    def __init__(self, library, directory, ext, start, end):
        BaseHook.__init__(self, library, directory, ext, start, end)

    def execute(self):
        if not Maya.load_plugin("redshift4maya.mll"):
            self.append_error("Load redshift4maya.mll failed.")
            return
        if not self.files:
            self.append_error("No rs files found")
            return
        file_num = len(self.files)
        if file_num == 1:
            file_name = self.files[0]
        else:
            frame_padding = self.frame_padding(self.files[0], "rs")
            file_name = re.sub("\d+\.rs$", "%s.rs" % ("#"*frame_padding), self.files[0])
        node = Maya.import_rs(file_name)
        if file_num > 1:
            mc.setAttr("%s.useFrameExtension" % node, True)
            exp = mc.createNode("expression", name="expression")
            mc.connectAttr("%s.out[0]" % exp, "%s.frameExtension" % node, f=1)
            mc.expression(exp, e=1, s="{0}.frameExtension=(frame-1)%{1}+1".format(node, file_num), ae=1, uc="all")

    def frame_padding(self, file_name, ext):
        """
        get frame padding of a file
        :param file_name:
        :param ext: file ext
        :return:
        """
        padding = 0
        pattern = ".*\D(\d+)\.%s" % ext
        padding_list = re.findall(pattern, file_name)
        if padding_list:
            padding = len(padding_list[0])
        return padding