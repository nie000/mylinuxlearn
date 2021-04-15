# -*- coding: utf-8 -*-
from MayaLib.maya_import_export.BaseHook import BaseHook

from MayaLib import Maya


class Hook(BaseHook):
    def __init__(self, library, directory, ext, start, end):
        BaseHook.__init__(self, library, directory, ext, start, end)

    def execute(self):
        files = self.files
        if not files:
            self.append_error("No .obj files found.")
            return
        Maya.maya_import(files[0])
