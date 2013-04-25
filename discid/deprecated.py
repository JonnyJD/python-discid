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
# Please submit bug reports to GitHub:
# https://github.com/JonnyJD/python-discid/issues
"""Deprecated functions and classes
"""

from warnings import warn, simplefilter

from discid.disc import Disc

# turn on DeprecationWarnings for DiscId below
simplefilter(action="once", category=DeprecationWarning)


class DiscId(Disc):
    """Deprecated class, use :func:`read` or :func:`put` or :class:`Disc`.
    """

    def __init__(self):
        warn("The DiscId class is deprecated.\n"
             "Use read/put on module level or Disc:",
             DeprecationWarning, stacklevel=2)
        Disc.__init__(self)
