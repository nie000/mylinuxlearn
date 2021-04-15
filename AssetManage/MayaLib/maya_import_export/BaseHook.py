# -*- coding: utf-8 -*-
import glob
import logging

from lib.path import Path


class BaseHook(object):
    logger = logging.getLogger("Hook")

    def __init__(self, library, directory, ext, start, end):
        """
        :param library: a library name
        :param directory: a toolset directory
        :param ext: file extention eg. ".ma", ".nk", ".otl"
        :param start: start frame
        :param end: end frame
        :return:
        """
        self.library = library
        self.directory = directory
        self.ext = ext
        self.start = start
        self.end = end
        self.__error_list = list()

    def append_error(self, error_str):
        """
        appen error content.
        :param error_str: str
        :return:
        """
        self.__error_list.append(error_str)

    def create_folder(self):
        """
        create toolset directory
        :return: None
        """
        Path(self.directory).create()

    @property
    def error_str(self):
        """
        error string
        :return:
        """
        return "\n".join(self.__error_list)

    @property
    def name(self):
        """
        current toolset name
        :return: str
        """
        return Path(self.directory).basename()

    @property
    def location(self):
        """
        the location you want to save. folder name is ext.
        :return: str
        """
        folder_name = self.ext.split(".")[-1]
        _location = "{directory}/{folder_name}".format(directory=self.directory, folder_name=folder_name)
        _location = _location.replace("\\", "/")
        return _location

    @property
    def texture_dir(self):
        _dir = "{0}/texture".format(self.directory)
        _dir = _dir.replace("\\", "/")
        return _dir

    @property
    def file(self):
        """
        the file you wanted. single frame.
        :return: str
        """
        _file = "{0}/{1}{2}".format(self.location, self.name, self.ext)
        _file = _file.replace("\\", "/")
        return _file

    @property
    def files(self):
        """
        the files you wanted. sequence.
        :return: list
        """
        if self.ext == ".files":
            _files = Path(self.location).children()
        else:
            _files = glob.glob("%s/*%s" % (self.location, self.ext))
        _files = [f.replace("\\", "/") for f in _files]
        return _files

    @property
    def thumbnail(self):
        """
        thumbnail path
        :return:
        """
        return "{0}/thumbnail.png".format(self.directory)

    def info_path(self):
        """
        info.json path
        :return:
        """
        return "{0}/info.json".format(self.directory)

    def remove_location(self):
        """
        before execute, you'd better remove the old
        :return:
        """
        Path(self.location).remove()

    def remove_thumbnail(self):
        """
        after execute, you'd better remove the old thumbnail
        :return:
        """
        Path(self.thumbnail).remove()

    def execute(self):
        """
        what need to do
        :return:
        """
        pass

    def main(self):
        """
        main function
        :return:
        """
        self.execute()
        if self.error_str:
            self.logger.error(self.error_str)
