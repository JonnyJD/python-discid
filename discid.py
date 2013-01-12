import os
import sys
from ctypes import *
from ctypes.util import find_library


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

    def read(self, device=None):
        c_device = c_char_p(device)
        # return defined as c_int, but used like c_bool
        c_return = c_bool(_lib.discid_read(self.__handle, c_device))
        self.__success = c_return.value
        return c_return.value

    def get_id(self):
        c_return = c_char_p(_lib.discid_get_id(self.__handle))
        return c_return.value

    def free(self):
        _lib.discid_free(self.__handle)
        self.__handle = None
    
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.free()


# vim:set shiftwidth=4 smarttab expandtab:
