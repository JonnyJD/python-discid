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
"""Track class
"""

from ctypes import c_int, c_void_p, c_char_p

from discid.libdiscid import _LIB
from discid.util import _decode


class Track(object):
    """Track objects are part of the :class:`Disc` class.
    """

    def __init__(self, disc, number):
        self._disc = disc
        self._number = number
        assert self._disc._handle.value is not None

    def __str__(self):
        if self._disc._success:
            return str(self.number)
        else:
            return ""

    _LIB.discid_get_track_offset.argtypes = (c_void_p, c_int)
    _LIB.discid_get_track_offset.restype = c_int
    def _get_track_offset(self):
        return _LIB.discid_get_track_offset(self._disc._handle, self.number)

    _LIB.discid_get_track_length.argtypes = (c_void_p, c_int)
    _LIB.discid_get_track_length.restype = c_int
    def _get_track_length(self):
        return _LIB.discid_get_track_length(self._disc._handle, self.number)

    try:
        _LIB.discid_get_track_isrc.argtypes = (c_void_p, c_int)
        _LIB.discid_get_track_isrc.restype = c_char_p
    except AttributeError:
        pass
    def _get_track_isrc(self):
        if self._disc._success and "isrc" in self._disc._requested_features:
            try:
                result = _LIB.discid_get_track_isrc(self._disc._handle,
                                                    self.number)
            except AttributeError:
                return None
            else:
                return _decode(result)
        else:
            return None

    @property
    def number(self):
        """The track number"""
        return self._number

    @property
    def offset(self):
        """The track offset"""
        return self._get_track_offset()

    @property
    def length(self):
        """The track length"""
        return self._get_track_length()

    @property
    def isrc(self):
        """The International Standard Recording Code

        This will be `None` when isrcs were not requested or not supported.
        """
        return self._get_track_isrc()


# vim:set shiftwidth=4 smarttab expandtab:
