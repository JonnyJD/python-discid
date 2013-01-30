Download and Installation
=========================

Dependencies
------------

**python-discid** works with Python 2 >= 2.6, or Python 3 >= 3.1.

The module :mod:`discid` cannot be imported without `Libdiscid`_ installed.

Package Repositories (Linux)
----------------------------

If you are using Linux,
you might find **python-discid** in a repository used by your package manager.

These packages are known:

 * Arch Linux:
   AUR (
   `Python 2 <https://aur.archlinux.org/packages/python2-discid/>`_,
   `Python 3 <https://aur.archlinux.org/packages/python-discid/>`_
   )
 * openSUSE:
   `software.opensuse.org <http://software.opensuse.org/package/python-discid>`_
 * Ubuntu:
   `PPA <https://launchpad.net/~jonnyjd/+archive/python-discid>`_

Your package manager will also handle the *libdiscid* dependency automatically.

PyPI
----

The next-best option is to load the Package from
`pypi <http://pypi.python.org/pypi/discid>`_
with `pip <http://www.pip-installer.org/>`_::

 pip install discid

You still have to install `Libdiscid`_.

Source Code
-----------

The code is available from `Github`_
as :source_download:`zip` and :source_download:`tar.gz`.

You can always get the latest code with :command:`git`::

 git clone https://github.com/JonnyJD/python-discid.git

Installation
************

You can use **python-discid** already when you put the :file:`discid.py`
in the same location you run your script from
or somewhere in your :envvar:`PYTHONPATH`.

System-wide installation is done with::

 python setup.py install

You can test your setup (including `Libdiscid`_) with::

 python setup.py test

.. _Github: https://github.com/JonnyJD/python-discid

Libdiscid
---------

If you don't have a package manager
that takes care of the *Libdiscid* dependency,
you have to download it manually.

You can find several builds at http://musicbrainz.org/doc/libdiscid.

If no build for your platform is available,
you have to get the source
as :libdiscid_download:`zip` or :libdiscid_download:`tar.gz`
and install with::

 cmake .
 make
 make install

If the last step doesn't work for you,
you might have to place the :file:`.DLL`, :file:`.dylib` or :file:`.so`
(depending on your platform)
in the same directory as you start your script from
or somewhere in your :envvar:`PATH`.
