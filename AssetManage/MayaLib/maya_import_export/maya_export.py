# -*- coding: utf-8 -*-
import maya.cmds as mc
from MayaLib.maya_import_export.BaseHook import BaseHook

from MayaLib import Maya


class Hook(BaseHook):
    def __init__(self, library, directory, ext, start, end):
        BaseHook.__init__(self, library, directory, ext, start, end)

    def execute(self):
        """
        :return: None
        """
        self.remove_location()

        if self.library in ["MayaShader"]:
            self.export_maya_shader()
        elif self.library in ["MayaAsset"]:
            self.export_maya_asset()
        elif self.library in ["MayaLight", "MayaVfx"]:
            self.export_maya_selected_node()
        else:
            Maya.export_selected(self.file, False)

    def export_maya_shader(self):
        """
        export textures and sg nodes
        :return:
        """
        selected = Maya.selected()
        if len(selected) > 1:
            self.append_error("More than one object selected.")
            return
        sg_node = Maya.get_sg_node_of_selected()
        if not sg_node:
            self.append_error("No shadingEngine node found. ")
            return
        if len(sg_node) > 1:
            self.append_error("More than one shadingEngine node assign to this selected object.")
            return
        texture_nodes = Maya.get_history_texture_nodes(sg_node)
        temp_dict = Maya.export_textures(texture_nodes, self.texture_dir)
        mc.select(sg_node, ne=1, r=1)
        Maya.export_selected(self.file, False)
        Maya.post_export_textures(temp_dict)

    def export_maya_asset(self):
        """
        export selected objects' textures and selected objects
        :return:
        """
        texture_nodes = Maya.get_texture_node_of_selected_geo()
        temp_dict = Maya.export_textures(texture_nodes, self.texture_dir)
        Maya.export_selected(self.file, False)
        Maya.post_export_textures(temp_dict)

    def export_maya_selected_node(self):
        """
        export selected node textures and selected node
        :return:
        """
        selected = Maya.selected()
        texture_nodes = Maya.get_history_texture_nodes(selected)
        temp_dict = Maya.export_textures(texture_nodes, self.texture_dir)
        Maya.export_selected(self.file, False)
        Maya.post_export_textures(temp_dict)
