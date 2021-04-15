# -*- coding: utf-8 -*-
import os
from MayaLib.maya_import_export.BaseHook import BaseHook

from MayaLib import Maya


class Hook(BaseHook):
    def __init__(self, library, directory, ext, start, end):
        BaseHook.__init__(self, library, directory, ext, start, end)

    def execute(self):
        if not Maya.load_plugin("AbcImport.mll"):
            self.append_error("Load AbcImport.mll failed.")
            return
        if not os.path.isfile(self.file):
            self.append_error("%s is not an exist file." % self.file)
            return
        Maya.import_abc(self.file)
