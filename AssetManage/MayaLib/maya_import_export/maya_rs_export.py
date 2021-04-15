# -*- coding: utf-8 -*-
from MayaLib.maya_import_export.BaseHook import BaseHook

from MayaLib import Maya


class Hook(BaseHook):
    def __init__(self, library, directory, ext, start, end):
        BaseHook.__init__(self, library, directory, ext, start, end)

    def execute(self):
        """
        :return: None
        """
        if not Maya.load_plugin("redshift4maya.mll"):
            print "Load redshift4maya.mll failed."
            return
        self.remove_location()
        texture_nodes = Maya.get_texture_node_of_selected_geo()
        temp_dict = Maya.export_textures(texture_nodes, self.texture_dir)
        Maya.export_rs(self.file, self.start, self.end)
        Maya.post_export_textures(temp_dict)

