# -*- coding: utf-8 -*-
import os
from MayaLib.maya_import_export.BaseHook import BaseHook

from MayaLib import Maya


class Hook(BaseHook):
    def __init__(self, library, directory, ext, start, end):
        BaseHook.__init__(self, library, directory, ext, start, end)

    def execute(self):
        f = self.file
        if not os.path.isfile(f):
            self.append_error("%s is not an exist file." % f)
            return
        Maya.maya_import(f)
