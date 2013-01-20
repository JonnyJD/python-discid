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
"""Python binding of Libdiscid

Libdiscid is a library to calculate MusicBrainz DiscIds
"""

import os
import sys
import ctypes
from ctypes import c_int, c_void_p, c_char_p
from ctypes.util import find_library


_version = "0.2.0-beta"
_base_name = "discid"

def __find_library(name):
    windows_names = ["%s.dll" % name, "lib%s.dll" % name, "lib%s-0.dll" % name]

    lib_file = find_library(name)

    if lib_file is None and sys.platform == "win32":
        for lib_name in windows_names:
            if lib_file is None:
                lib_file = find_library(lib_name)

    if lib_file is not None:
        return lib_file
    else:
        if sys.platform.startswith == "linux":
            return "lib%s.so.0" % name
        elif sys.platform == "darwin":
            return "lib%s.0.dylib" % name
        elif sys.platform == "cygwin":
            return "cyg%name-0.dll" % name
        elif sys.platform == "win32":
            for lib_name in windows_names:
                if os.path.isfile(lib_name):
                    return lib_name
            return "%s.dll" % name
        else:
            return "lib%s.so.0" % name

def __open_library(lib_name=None):
    if lib_name is None:
        _lib_name = __find_library()
    else:
        _lib_name = lib_name
    assert _lib_name is not None
    try:
        return ctypes.cdll.LoadLibrary(_lib_name)
    except OSError as e:
        raise ImportError(e)

_lib_name = __find_library(_base_name)
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


_lib.discid_get_default_device.argtypes = ()
_lib.discid_get_default_device.restype = c_char_p
def __get_default_device():
    device = _lib.discid_get_default_device()
    return _decode(device)

DEFAULT_DEVICE = __get_default_device()

class DiscError(IOError):
    pass


class DiscId(object):

    _lib.discid_new.argtypes = ()
    _lib.discid_new.restype = c_void_p
    def __init__(self):
        self.__handle = c_void_p(_lib.discid_new())
        self.__success = False
        assert self.__handle.value is not None

    def __str__(self):
        if self.__success:
            return self.get_id()
        else:
            return ""

    _lib.discid_get_error_msg.argtypes = (c_void_p, )
    _lib.discid_get_error_msg.resype = c_char_p
    def __get_error_msg(self):
        error = _lib.discid_get_error_msg(self.__handle)
        return _decode(error)


    _lib.discid_read.argtypes = (c_void_p, c_char_p)
    _lib.discid_read.restype = c_int
    def read(self, device=None):
        # device = None will use the default device (internally)
        result = _lib.discid_read(self.__handle, _encode(device)) == 1
        self.__success = result
        if not self.__success:
            raise DiscError(self.__get_error_msg())
        return self.__success

    _lib.discid_get_id.argtypes = (c_void_p, )
    _lib.discid_get_id.restype = c_char_p
    def __get_id(self):
        if self.__success:
            result = _lib.discid_get_id(self.__handle)
            return _decode(result)
        else:
            return None

    id = property(__get_id, None, None, "MusicBrainz DiscId")

    _lib.discid_free.argtypes = (c_void_p, )
    _lib.discid_free.restype = None
    def free(self):
        _lib.discid_free(self.__handle)
        self.__handle = None
    
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.free()


# vim:set shiftwidth=4 smarttab expandtab:
