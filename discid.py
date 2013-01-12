# Copyright (C) 2013  Johannes Dewender
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from ctypes import *
from ctypes.util import find_library


_version = "0.1.0"

def __find_library():
    windows_names = ["discid.dll", "libdiscid.dll", "libdiscid-0.dll"]

    lib_file = find_library("discid")

    if lib_file is None and sys.platform == "win32":
        for lib_name in windows_names:
            if lib_file is None:
                lib_file = find_library(lib_name)

    if lib_file is not None:
        return lib_file
    else:
        if sys.platform.startswith == "linux":
            return "libdiscid.so.0"
        elif sys.platform == "darwin":
            return "libdiscid.0.dylib"
        elif sys.platform == "cygwin":
            return "cygdiscid-0.dll"
        elif sys.platform == "win32":
            for lib_name in windows_names:
                if os.path.isfile(lib_name):
                    return lib_name
            return "discid.dll"
        else:
            return "libdiscid.so.0"

def __open_library(lib_name=None):
    if lib_name is None:
        _lib_name = __find_library()
    else:
        _lib_name = lib_name
    assert _lib_name is not None
    try:
        return cdll.LoadLibrary(_lib_name)
    except OSError as e:
        raise ImportError(e)

_lib_name = __find_library()
_lib = __open_library(_lib_name)


def _encode(string):
    try:
        return string.encode()
    except AttributeError:
        # already byte string (Python 3)
        return string
    # UnicodeDecodeError (Python 2) is NOT catched
    # device names should be ascii

def _decode(byte_string):
    return byte_string.decode()


class DiscError(IOError):
    pass


class DiscId(object):
    def __init__(self):
        self.__handle = c_void_p(_lib.discid_new())
        self.__success = False
        assert self.__handle.value is not None

    def __str__(self):
        if self.__success:
            return self.get_id()
        else:
            return ""

    def __get_error_msg(self):
        c_error = c_char_p(_lib.discid_get_error_msg(self.__handle))
        return _decode(c_error.value)


    def read(self, device=None):
        c_device = c_char_p(_encode(device))
        # return defined as c_int, but used like c_bool
        c_return = c_bool(_lib.discid_read(self.__handle, c_device))
        self.__success = c_return.value
        if not self.__success:
            raise DiscError(self.__get_error_msg())
        return self.__success

    def get_id(self):
        if self.__success:
            c_return = c_char_p(_lib.discid_get_id(self.__handle))
            return _decode(c_return.value)
        else:
            return None

    def free(self):
        _lib.discid_free(self.__handle)
        self.__handle = None
    
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.free()


# vim:set shiftwidth=4 smarttab expandtab:
