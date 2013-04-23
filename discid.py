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

The user is expected to create a :class:`DiscId` object
using :func:`read` or :func:`put` and extract the generated information.

Importing this module will open libdiscid at the same time
and will raise :exc:`OSError` when libdiscid is not found.
"""

import os
import sys
import ctypes
from ctypes import c_int, c_void_p, c_char_p, c_uint
from ctypes.util import find_library


__version__ = "0.4.0-dev"

_LIB_BASE_NAME = "discid"
_LIB_MAJOR_VERSION = 0

# our implemented of libdiscid's enum discid_feature
_FEATURE_MAPPING = {"read": 1 << 0, "mcn": 1 << 1, "isrc": 1 << 2}


def _find_library(name, version=0):
    """Find a library by base-name and major version
    """
    windows_names = ["%s.dll" % name, "lib%s.dll" % name,
                     "lib%s-%d.dll" % (name, version)]

    lib_file = None

    # force prefer current folder
    # for linux/UNIX-like and Windows
    if sys.platform in ["darwin", "cygwin"]:
        # these will already work fine with find_library
        pass
    elif sys.platform == "win32":
        for lib_name in windows_names:
            if os.path.isfile(lib_name):
                lib_file = lib_name
                break
    else:
        # that would be linux/UNIX-like
        # these need to prepend ./
        lib_name = "./lib%s.so.%d" % (name, version)
        if os.path.isfile(lib_name):
            lib_file = lib_name

    # doesn't work on Windows
    # Darwin gives a full path when found system-wide
    # Linux and Cygwin give base filename when found
    # Darwin and Cygwin will find and prefer in current folder
    if lib_file is None:
        lib_file = find_library(name)

    # Windows needs complete filenames  
    # and gives a full path when found system-wide
    # also searches in current folder, but system-wide preferred
    if lib_file is None and sys.platform == "win32":
        for lib_name in windows_names:
            if lib_file is None:
                lib_file = find_library(lib_name)

    if lib_file is None:
        # this won't help anymore,
        # but gives a nice platform dependent file in the error message
        if sys.platform == "win32":
            lib_file = "%s.dll" % name
        elif sys.platform == "darwin":
            lib_file = "lib%s.%d.dylib" % (name, version)
        elif sys.platform == "cygwin":
            lib_file = "cyg%s-%d.dll" % (name, version)
        else:
            lib_file = "lib%s.so.%d" % (name, version)

    return lib_file

def _open_library(lib_name):
    """Open a library by name or location
    """
    try:
        return ctypes.cdll.LoadLibrary(lib_name)
    except OSError as exc:
        if lib_name not in str(exc):
            # replace uninformative Error on Windows
            raise OSError("could not find libdiscid: %s" % lib_name)
        else:
            raise

_LIB_NAME = _find_library(_LIB_BASE_NAME, _LIB_MAJOR_VERSION)
_LIB = _open_library(_LIB_NAME)


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
def _get_default_device():
    """Get the default device for the platform
    """
    device = _LIB.discid_get_default_device()
    if type(device) == type(b"test"):
        return _decode(device)
    else:
        # probably Mocked for sphinx
        return None

try:
    _LIB.discid_get_feature_list.argtypes = (c_void_p, )
    _LIB.discid_get_feature_list.restype = None
except AttributeError:
    _features_available = False
else:
    _features_available = True
def _get_features():
    """Get the supported features for the platform.
    """
    features = []
    if _features_available:
        c_features = (c_char_p * 32)()
        _LIB.discid_get_feature_list(c_features)
        for feature in c_features:
            if feature:
                features.append(_decode(feature))
    else:
        # libdiscid <= 0.4.0
        features = ["read"]     # no generic platform yet
        try:
            # test for ISRC/MCN API (introduced 0.3.0)
            _LIB.discid_get_mcn
        except AttributeError:
            pass
        else:
            # ISRC/MCN API found -> libdiscid = 0.3.x
            if (sys.platform.startswith("linux") and
                    not os.path.isfile("/usr/lib/libdiscid.so.0.3.0")
                    and not os.path.isfile("/usr/lib64/libdiscid.so.0.3.0")):
                features += ["mcn", "isrc"]
            elif sys.platform in ["darwin", "win32"]:
                features += ["mcn", "isrc"]

    return features

DEFAULT_DEVICE = _get_default_device()
"""The default device to use for :func:`read` on this platform
given as a :obj:`unicode` or :obj:`str <python:str>` object.
"""

FEATURES = _get_features()
"""The features libdiscid supports for the platform as a list of strings.
Some Functions can raise :exc:`NotImplementedError` when a feature
is not available.
Some features might not be implemented in this python module,
see :data:`FEATURES_IMPLEMENTED`.
"""

FEATURES_IMPLEMENTED = list(_FEATURE_MAPPING.keys())
"""The features implemented in this python module as a list of strings.
Some might not be available for your platform, see :data:`FEATURES`.
"""

def read(device=None, features=[]):
    """Reads the TOC from the device given as string
    and returns a :class:`DiscId` object.

    That string can be either of:
    :obj:`str <python:str>`, :obj:`unicode` or :obj:`bytes`.
    However, it should in no case contain non-ASCII characters.
    If no device is given, the :data:`DEFAULT_DEVICE` is used.

    You can optionally add a subset of the features in
    :data:`FEATURES` or the whole list to read more than just the TOC.
    In contrast to libdiscid, :func:`read` won't read any
    of the additional features by default.

    A :exc:`DiscError` exception is raised when the reading fails,
    and :exc:`NotImplementedError` when libdiscid doesn't support
    reading discs on the current platform.
    """
    disc = DiscId()
    disc.read(device)
    return disc

def put(first, last, offsets):
    """Creates a TOC based on the offsets given
    and resturns a :class:`DiscId` object.

    Takes the *first* and *last* **audio** tracks as :obj:`int` and
    *offsets* is supposed to be the same as :attr:`track_offsets`.
    That is: ``offsets[0]`` are the total number of sectors
    and the following are the offsets of each track.
    """
    disc = DiscId()
    disc.put(first, last, offsets)
    return disc

class DiscError(IOError):
    """:func:`read` will raise this exception when an error occured.
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
        self._handle = c_void_p(_LIB.discid_new())
        self._success = False
        self._requested_features = []
        assert self._handle.value is not None

    def __str__(self):
        if self._success:
            return self.id
        else:
            return ""

    _LIB.discid_get_error_msg.argtypes = (c_void_p, )
    _LIB.discid_get_error_msg.restype = c_char_p
    def _get_error_msg(self):
        """Get the error message for the last error with the object.
        """
        error = _LIB.discid_get_error_msg(self._handle)
        return _decode(error)


    _LIB.discid_read.argtypes = (c_void_p, c_char_p)
    _LIB.discid_read.restype = c_int
    try:
        _LIB.discid_read_sparse.argtypes = (c_void_p, c_char_p, c_uint)
        _LIB.discid_read_sparse.restype = c_int
    except AttributeError:
        pass
    def read(self, device=None, features=[]):
        """Reads the TOC from the device given as string

        The user is supposed to use :func:`discid.read`.
        """
        if "read" not in FEATURES:
            raise NotImplementedError("discid_read not implemented on platform")

        # only use features implemented on this platform and in this module
        self._requested_features = list(set(features) & set(FEATURES)
                                        & set(FEATURES_IMPLEMENTED))

        # create the bitmask for libdiscid
        c_features = 0
        for feature in features:
            c_features += _FEATURE_MAPPING.get(feature, 0)

        # device = None will use the default device (internally)
        try:
            result = _LIB.discid_read_sparse(self._handle, _encode(device),
                                             c_features) == 1
        except AttributeError:
            result = _LIB.discid_read(self._handle, _encode(device)) == 1
        self._success = result
        if not self._success:
            raise DiscError(self._get_error_msg())
        return self._success

    _LIB.discid_put.argtypes = (c_void_p, c_int, c_int, c_void_p)
    _LIB.discid_put.restype = c_int
    # TODO: test if input is valid (int rather than string, ...)
    def put(self, first, last, offsets):
        """Creates a TOC based on the offsets given.

        The user is supposed to use :func:`discid.put`.
        """
        # only the "read" (= TOC) feature is supported by put
        self._requested_features = ["read"]

        c_offsets = (c_int * len(offsets))(*tuple(offsets))
        result = _LIB.discid_put(self._handle, first, last, c_offsets) == 1
        self._success = result
        if not self._success:
            # TODO: should that be the same Exception as for read()?
            # should that be TOCError?
            raise DiscError(self._get_error_msg())
        return self._success


    _LIB.discid_get_id.argtypes = (c_void_p, )
    _LIB.discid_get_id.restype = c_char_p
    def _get_id(self):
        """Gets the current MusicBrainz disc ID
        """
        if self._success:
            result = _LIB.discid_get_id(self._handle)
            return _decode(result)
        else:
            return None

    _LIB.discid_get_freedb_id.argtypes = (c_void_p, )
    _LIB.discid_get_freedb_id.restype = c_char_p
    def _get_freedb_id(self):
        """Gets the current FreeDB disc ID
        """
        if self._success:
            result = _LIB.discid_get_freedb_id(self._handle)
            return _decode(result)
        else:
            return None

    _LIB.discid_get_submission_url.argtypes = (c_void_p, )
    _LIB.discid_get_submission_url.restype = c_char_p
    def _get_submission_url(self):
        """Give an URL to submit the current TOC
        as a new Disc ID to MusicBrainz.
        """
        if self._success:
            result = _LIB.discid_get_submission_url(self._handle)
            return _decode(result)
        else:
            return None

    _LIB.discid_get_webservice_url.argtypes = (c_void_p, )
    _LIB.discid_get_webservice_url.restype = c_char_p
    def _get_webservice_url(self):
        """Give an URL to retrieve information about the CD from MusicBrainz.
        """
        if self._success:
            result = _LIB.discid_get_webservice_url(self._handle)
            return _decode(result)
        else:
            return None

    _LIB.discid_get_first_track_num.argtypes = (c_void_p, )
    _LIB.discid_get_first_track_num.restype = c_int
    def _get_first_track_num(self):
        """Gets the first track number
        """
        return _LIB.discid_get_first_track_num(self._handle)

    _LIB.discid_get_last_track_num.argtypes = (c_void_p, )
    _LIB.discid_get_last_track_num.restype = c_int
    def _get_last_track_num(self):
        """Gets the last track number
        """
        return _LIB.discid_get_last_track_num(self._handle)

    _LIB.discid_get_sectors.argtypes = (c_void_p, )
    _LIB.discid_get_sectors.restype = c_int
    def _get_sectors(self):
        """Gets the total number of sectors on the disc
        """
        return _LIB.discid_get_sectors(self._handle)

    _LIB.discid_get_track_offset.argtypes = (c_void_p, c_int)
    _LIB.discid_get_track_offset.restype = c_int
    def _get_track_offset(self, track_number):
        """Gets the offset for a specific track
        """
        return _LIB.discid_get_track_offset(self._handle, track_number)

    def _get_track_offsets(self):
        """Generates the list of offsets,
        starting with the total number of sectors
        """
        offsets = []
        offsets.append(self.sectors)
        for track_number in range(1, self.first_track_num):
            offsets.append(None)
        for track_number in range(self.first_track_num,
                                  self.last_track_num + 1):
            offset = self._get_track_offset(track_number)
            offsets.append(offset)
        return offsets

    _LIB.discid_get_track_length.argtypes = (c_void_p, c_int)
    _LIB.discid_get_track_length.restype = c_int
    def _get_track_length(self, track_number):
        """Gets the length for a specific track
        """
        return _LIB.discid_get_track_length(self._handle, track_number)

    def _get_track_lengths(self):
        """Generates the list of lengths,
        starting with the lengths of the first pregap
        """
        lengths = []
        lengths.append(self.track_offsets[1])
        for track_number in range(1, self.first_track_num):
            lengths.append(None)
        for track_number in range(self.first_track_num,
                                  self.last_track_num + 1):
            length = self._get_track_length(track_number)
            lengths.append(length)
        return lengths

    try:
        _LIB.discid_get_mcn.argtypes = (c_void_p, )
        _LIB.discid_get_mcn.restype = c_char_p
    except AttributeError:
        pass
    def _get_mcn(self):
        """Gets the current Media Catalogue Number (MCN/UPC/EAN)
        """
        if self._success and "mcn" in self._requested_features:
            try:
                result = _LIB.discid_get_mcn(self._handle)
            except AttributeError:
                return None
            else:
                return _decode(result)
        else:
            return None

    try:
        _LIB.discid_get_track_isrc.argtypes = (c_void_p, c_int)
        _LIB.discid_get_track_isrc.restype = c_char_p
    except AttributeError:
        pass
    def _get_track_isrc(self, track_number):
        """Gets the ISRC for a specific track
        """
        try:
            result = _LIB.discid_get_track_isrc(self._handle, track_number)
        except AttributeError:
            return None
        else:
            return _decode(result)

    def _get_track_isrcs(self):
        """Generates the list of ISRCs,
        starting with the MCN of the disc as elemnt 0
        """
        isrcs = []
        if self._success and "isrc" in self._requested_features:
            isrcs.append(self.mcn)
            for track_number in range(1, self.first_track_num):
                isrcs.append(None)
            for track_number in range(self.first_track_num,
                                      self.last_track_num + 1):
                isrc = self._get_track_isrc(track_number)
                isrcs.append(isrc)
        return isrcs

    id = property(_get_id, None, None, "MusicBrainz disc ID")
    """This is the MusicBrainz :musicbrainz:`Disc ID`.

    It is set after a the TOC was populated or :obj:`None`.
    If set, this is a :obj:`unicode` or :obj:`str <python:str>` object.
    """

    freedb_id = property(_get_freedb_id, None, None, "FreeDB disc ID")
    """This is the :musicbrainz:`FreeDB` Disc ID (without category).

    It is set after a the TOC was populated or :obj:`None`.
    If set, this is a :obj:`unicode` or :obj:`str <python:str>` object.
    """

    submission_url = property(_get_submission_url, None, None,
                              "Disc ID / TOC Submission URL for MusicBrainz")
    """With this url you can submit the current TOC
    as a new MusicBrainz :musicbrainz:`Disc ID`.

    If there is no populated TOC the url is :obj:`None`.
    Otherwise this is a :obj:`unicode` or :obj:`str <python:str>` object.
    """

    webservice_url = property(_get_webservice_url, None, None,
                              "web service URL for info about the CD")
    """With this url you can retrive information about the CD in XML
    from the MusicBrainz web service.

    If there is no populated TOC the url is :obj:`None`.
    Otherwise this is a :obj:`unicode` or :obj:`str <python:str>` object.
    """
    last_track_num = property(_get_last_track_num, None, None,
                              "Number of the last **audio** track")

    first_track_num = property(_get_first_track_num, None, None,
                              "Number of the first track")

    sectors = property(_get_sectors, None, None,
                              "Total sector count")

    track_offsets = property(_get_track_offsets, None, None,
                              "List of offsets, track_offsets[0] == sectors")
    """A list of all track offsets.

    The first element is the leadout track
    and contains the total number of sectors on the disc.
    The following elements are the offsets for all **audio** tracks.
    ``track_offsets[i]`` is the offset for the i-th track (as :obj:`int`).
    """

    track_lengths = property(_get_track_lengths, None, None,
                              "List of lengths, track_lengths[0] == 1st pregap")
    """A list of all track lengths.

    The first element is the length of the pregap of the first track.
    The following elements are the lengths for all **audio** tracks.
    ``track_length[i]`` is the length for the i-th track (as :obj:`int`).
    """

    mcn = property(_get_mcn, None, None, "Media Catalogue Number")
    """This is the Media Catalogue Number (MCN/UPC/EAN)

    It is set after a the "mcn" feature was requested on a read
    and supported by the platform or :obj:`None`.
    If set, this is a :obj:`unicode` or :obj:`str <python:str>` object.
    """

    track_isrcs = property(_get_track_isrcs, None, None,
                              "List of ISRCs, track_isrcs[0] == mcn")
    """A list of all track ISRCs.

    The first element is the MCN of the disc.
    The following elements are the isrcs for all **audio** tracks.
    If no ISRC was found, it is the empty string.
    If no ISRCs were requested or the feature is not available,
    this will be the empty list.
    ``track_isrcs[i]`` is the ISRC for the i-th track (as :obj:`int`).
    """


    _LIB.discid_free.argtypes = (c_void_p, )
    _LIB.discid_free.restype = None
    def _free(self):
        """This will free the internal allocated memory for the object.
        """
        _LIB.discid_free(self._handle)
        self._handle = None
    
    def __enter__(self):
        """deprecated :keyword:`with` usage"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """deprecated :keyword:`with` usage"""
        pass

    def __del__(self):
        self._free()


# vim:set shiftwidth=4 smarttab expandtab:
