import os
from ctypes import *
from ctypes.util import find_library


def __find_library():
    if os.name == "posix":
        return find_library("discid")
    elif os.name == "nt":
        return "discid.dll"
    else:
        return "libdiscid.so.0"

def __open_library(lib_name):
    return cdll.LoadLibrary(lib_name)

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
