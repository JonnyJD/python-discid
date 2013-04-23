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

The user is expected to create a :class:`Disc` object
using :func:`read` or :func:`put` and extract the generated information.

Importing this module will open libdiscid at the same time
and will raise :exc:`OSError` when libdiscid is not found.
"""

from discid.disc import read, put, Disc, DiscError, FEATURES_IMPLEMENTED
from discid.libdiscid import DEFAULT_DEVICE, FEATURES

__version__ = "0.4.0-dev"


class DiscId(Disc):
    """Deprecated class, use :func:`read` or :func:`put` or :class:`Disc`.
    """

    def __init__(self):
        sys.stderr.write("\nWarning: The DiscId class is deprecated.\n")
        sys.stderr.write("         Use read/put on module level or Disc.\n")
        Disc.__init__(self)
