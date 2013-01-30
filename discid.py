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
#
# Please submit bug reports to Github:
# https://github.com/JonnyJD/python-discid/issues
"""Python binding of Libdiscid

Libdiscid is a library to calculate MusicBrainz Disc IDs.
This module provides a python-like API for that functionality.

The user is expected to create a :class:`DiscId` object,
feed it with some type of TOC and extract the generated information.
"""

import os
import sys
import ctypes
from ctypes import c_int, c_void_p, c_char_p
from ctypes.util import find_library


_VERSION = "0.2.0"
_BASE_NAME = "discid"


def __find_library(name):
    """Find a library by base-name
    """
    windows_names = ["%s.dll" % name, "lib%s.dll" % name, "lib%s-0.dll" % name]

    lib_file = find_library(name)

    if lib_file is None and sys.platform == "win32":
        for lib_name in windows_names:
            if lib_file is None:
                lib_file = find_library(lib_name)

    if lib_file is None:
        if sys.platform.startswith == "linux":
            lib_file = "lib%s.so.0" % name
        elif sys.platform == "darwin":
            lib_file = "lib%s.0.dylib" % name
        elif sys.platform == "cygwin":
            lib_file = "cyg%s-0.dll" % name
        elif sys.platform == "win32":
            for lib_name in windows_names:
                if os.path.isfile(lib_name):
                    lib_file = lib_name
                    break
            lib_file = "%s.dll" % name
        else:
            lib_file = "lib%s.so.0" % name
    return lib_file

def __open_library(lib_name):
    """Open a library by name or location
    """
    try:
        return ctypes.cdll.LoadLibrary(lib_name)
    except OSError as err:
        raise ImportError(err)

_LIB_NAME = __find_library(_BASE_NAME)
_LIB = __open_library(_LIB_NAME)


def _encode(string):
    """Encode (unicode) string to byte string
    """
    try:
        return string.encode()
    except AttributeError:
        # already byte string (Python 3)
        return string
    # UnicodeDecodeError (Python 2) is NOT catched
    # device names should be ascii

def _decode(byte_string):
    """Decode byte string to (unicode) string
    """
    return byte_string.decode()


_LIB.discid_get_default_device.argtypes = ()
_LIB.discid_get_default_device.restype = c_char_p
def __get_default_device():
    """Get the default device for the platform
    """
    device = _LIB.discid_get_default_device()
    if type(device) == type(b"test"):
        return _decode(device)
    else:
        # probably Mocked for sphinx
        return None

DEFAULT_DEVICE = __get_default_device()
"""The default device to use for :func:`DiscId.read` on this platform
given as a :obj:`unicode` or :obj:`str <python:str>` object.
"""

class DiscError(IOError):
    """:func:`DiscId.read` will raise this exception when an error occured.
    An error string (:obj:`unicode`/:obj:`str <python:str>`) is provided.
    """
    pass


class DiscId(object):
    """The main class of this module.
    """

    _LIB.discid_new.argtypes = ()
    _LIB.discid_new.restype = c_void_p
    def __init__(self):
        """The initialization will reserve some memory
        for internal data structures.
        """
        self.__handle = c_void_p(_LIB.discid_new())
        self.__success = False
        assert self.__handle.value is not None

    def __str__(self):
        if self.__success:
            return self.id
        else:
            return ""

    _LIB.discid_get_error_msg.argtypes = (c_void_p, )
    _LIB.discid_get_error_msg.restype = c_char_p
    def __get_error_msg(self):
        """Get the error message for the last error with the object.
        """
        error = _LIB.discid_get_error_msg(self.__handle)
        return _decode(error)


    _LIB.discid_read.argtypes = (c_void_p, c_char_p)
    _LIB.discid_read.restype = c_int
    def read(self, device=None):
        """Reads the TOC from the device given as string.

        That string can be either of:
        :obj:`str <python:str>`, :obj:`unicode` or :obj:`bytes`.
        However, it should in no case contain non-ASCII characters.

        A :exc:`DiscError` exception is raised when the reading fails.
        """
        # device = None will use the default device (internally)
        result = _LIB.discid_read(self.__handle, _encode(device)) == 1
        self.__success = result
        if not self.__success:
            raise DiscError(self.__get_error_msg())
        return self.__success

    _LIB.discid_get_id.argtypes = (c_void_p, )
    _LIB.discid_get_id.restype = c_char_p
    def __get_id(self):
        """Gets the current MusicBrainz DiscId
        """
        if self.__success:
            result = _LIB.discid_get_id(self.__handle)
            return _decode(result)
        else:
            return None

    id = property(__get_id, None, None, "MusicBrainz DiscId")
    """This is the MusicBrainz :musicbrainz:`Disc ID`.

    It is set after a successfull :func:`read` or :obj:`None`.
    If set, this is a :obj:`unicode` or :obj:`str <python:str>` object.
    """

    _LIB.discid_get_submission_url.argtypes = (c_void_p, )
    _LIB.discid_get_submission_url.restype = c_char_p
    def __get_submission_url(self):
        """Give an URL to submit the current TOC
        as a new Disc ID to MusicBrainz.
        """
        if self.__success:
            result = _LIB.discid_get_submission_url(self.__handle)
            return _decode(result)
        else:
            return None

    submission_url = property(__get_submission_url, None, None,
                              "Disc ID / TOC Submission URL for MusicBrainz")
    """With this url you can submit the current TOC
    as a new MusicBrainz :musicbrainz:`Disc ID`.

    If there was no successfull :func:`read` the url is :obj:`None`.
    Otherwise this is a :obj:`unicode` or :obj:`str <python:str>` object.
    """

    _LIB.discid_free.argtypes = (c_void_p, )
    _LIB.discid_free.restype = None
    def free(self):
        """This will free the internal allocated memory for the object.
        You can't use this object anymore afterwards.

        Please consider using the :keyword:`with` statement for the object,
        which will take care of this destruction automatically.
        """
        _LIB.discid_free(self.__handle)
        self.__handle = None
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.free()


# vim:set shiftwidth=4 smarttab expandtab:
