# -*- coding: utf-8 -*-
# @Author   : niejiali
# @Time     : 2018/10/17 14:55
# @File     : ControllerLibrary.py
# @Software : PyCharm
import json
import os
import maya.cmds as cmds

from assetsliber.lib.CreateDir import mk_dir


class ControllerLibrary(dict):

    def __init__(self, parent=None):
        self.path = ''

    def createDir(self, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)

    def save(self, **info):
        print(info), 123355
        directory = os.path.dirname(info['path'])
        mk_dir(directory)
        path = info['path']
        infoFile = info['json_path']
        cmds.file(rename=path)

        if cmds.ls(selection=True):
            cmds.file(force=True, exportSelected=True)
        else:
            cmds.file(save=True, force=True)

        self[info['name']] = info

        with open(infoFile, 'w') as f:
            json.dump(info, f, indent=4)

    def find(self, directory):
        if not os.path.exists(directory):
            return
        files = os.listdir(directory)
        for name in files:
            infoFile = name+'/%s.json' % name
            screenshot = name+'/%s.jpg' % name
            screenshot_png = name+'/%s.png' % name
            infoFile = os.path.join(directory, infoFile)
            if os.path.exists(infoFile):
                with open(infoFile, 'r') as f:
                    data = json.load(f)
            else:
                data = {}

            screenshot = os.path.join(directory, screenshot)
            screenshot_png = os.path.join(directory, screenshot_png)
            if os.path.exists(screenshot_png):
                data['screenshot'] = os.path.join(directory, screenshot_png)
            else:
                data['screenshot'] = os.path.join(directory, screenshot)
            data['name'] = name
            data['path'] = os.path.join(directory, name)
            self[name] = data

    def load(self, name):
        path = self[name]['path']
        cmds.file(path, i=True, usingNamespaces=False)

    def saveScreenshot(self, name, directory):
        path = os.path.join(directory, '%s.jpg' % name)

        cmds.viewFit()

        cmds.setAttr("defaultRenderGlobals.imageFormat", 8) # This is the value for jpeg

        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200,
                       showOrnaments=False, startTime=1, endTime=1, viewer=False)

        return path

    def join(self, path1, path2):
        return os.path.join(path1, path2)


if __name__ == '__main__':
    path = r'D:\assets\test'
    t = ControllerLibrary()
    t.find(path)
    for name, info in t.items():
        print name, info