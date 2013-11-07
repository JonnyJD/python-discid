python-discid |current|
=======================

**python-discid** is a Python binding
of :musicbrainz:`libdiscid` by MusicBrainz.

The main purpose is the calculation of an identifier for audio discs
(:musicbrainz:`Disc ID`) to use for the MusicBrainz_ database.
Additionally the disc MCN and track :musicbrainz:`ISRCs <ISRC>`
can be extracted.

This module is released under the
`GNU Lesser General Public License Version 3
<http://www.gnu.org/licenses/lgpl.html>`_ or later (LGPL3+) and
the code repository and the bug tracker are at GitHub_.

If you are interested in a binding for the MusicBrainz Web Service,
you might be interested in `python-musicbrainzngs`_.

Contents
--------
.. toctree::
   :maxdepth: 2

   install
   usage
   api
   CHANGES

Related Tools
-------------
There are other other bindings of libdiscid available.
Please check :musicbrainz:`Libdiscid`.

In particular there is another Python binding named `python-libdiscid`_.
The main difference is, that `python-libdiscid` is released
under the Expat license and uses Cython.
This means that it needs to be compiled against libdiscid.
`Python-discid` doesn't need compilation, as it uses :mod:`ctypes`.

If you want to use the disc ID created by `python-discid` to query
MusicBrainz for metatdata, then you should use `python-musicbrainzngs`_.
See :ref:`fetching_metadata` for using `discid` and `musicbrainzngs` together.

Indices and tables
------------------
* :ref:`genindex`
* :ref:`search`

.. _GitHub: https://github.com/JonnyJD/python-discid
.. _MusicBrainz: http://musicbrainz.org
.. _python-musicbrainzngs: https://python-musicbrainzngs.readthedocs.org/
.. _python-libdiscid: http://pythonhosted.org/python-libdiscid/
