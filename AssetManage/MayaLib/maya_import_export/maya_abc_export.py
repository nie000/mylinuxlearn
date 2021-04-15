# -*- coding: utf-8 -*-
import os
import maya.mel as mel
import pymel.core as pm
import maya.cmds as mc


def maya_abc_export(path, file_name):
    if not load_plugin("AbcExport.mll"):
        print "Load AbcExport.mll failed."
        return

    if not os.path.isdir(path):
        os.makedirs(path)
    camera = pm.ls(sl=True)[0]
    mel.eval('AbcExport -j \"-fameRange 1 120 -root |%s -file %s/%s.abc\";' % (camera, path, file_name))


def plugin_loaded(plugin):
    return mc.pluginInfo(plugin, q=1, loaded=1)


def load_plugin(plugin):
    if not plugin_loaded(plugin):
        mc.loadPlugin(plugin, quiet=1)
    return True

