# -*- coding: utf-8 -*-
import os
import maya.mel as mel
from MayaLib.maya_import_export.BaseHook import BaseHook


class Hook(BaseHook):
    def __init__(self, library, directory, ext, start, end):
        BaseHook.__init__(self, library, directory, ext, start, end)

    def execute(self):
        f = self.file
        if not os.path.isfile(f):
            self.append_error("%s is not an exist file." % f)
            return
        mel.eval("FBXImport -file \"%s\";" % f)
