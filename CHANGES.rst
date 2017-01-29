Changelog
=========

Changes in 1.1.1 (2017-01-29):
------------------------------
 * workaround :issue:`43` for py2app problems
 * :issue:`41` improve windows example

Changes in 1.1.0 (2013-10-09):
------------------------------
 * feature :issue:`36` add :attr:`Disc.toc_string`
 * :issue:`38` remove :class:`DiscId` (deprecated since 0.5.0)

Changes in 1.0.3 (2013-10-06):
------------------------------
 * fix: :issue:`37` test_emptyness: Assertion disc->success failed

Changes in 1.0.2 (2013-06-27):
------------------------------
 * revert code to version 1.0.0 (see :issue:`35`)
 * fix: :issue:`35` deprecation warning for DEFAULT_DEVICE shows always
 * renamed a api documentation page, a redirect was created

Changes in 1.0.1 (2013-06-26):
------------------------------
 * fix: :issue:`34` bring back :data:`DEFAULT_DEVICE` as deprecated

Changes in 1.0.0 (2013-06-25):
------------------------------
 * :issue:`30` :data:`DEFAULT_DEVICE` is now :func:`get_default_device()`
 * :issue:`32` :attr:`Disc.submission_url` doesn't point to a redirect now
 * fix: seconds are now rounded the same as on MB server (0.5->up)

Changes in 0.5.0 (2013-04-27):
------------------------------
 * feature: :issue:`10` add :attr:`Disc.mcn` and :attr:`Track.isrc`
 * feature: add :data:`LIBDISCID_VERSION_STRING`
 * feature: :issue:`28` add :attr:`Disc.seconds`, :attr:`Track.seconds`
   and aliases :attr:`Disc.length` and :attr:`Track.sectors`
 * :issue:`22` move :func:`read` and :func:`put` to module level
 * :issue:`25` provide a package `discid` rather than a module
 * :issue:`29` changed parameters for :func:`put` to include extra `sectors`
   and add :exc:`TOCError`
 * rename :class:`DiscId` to :class:`Disc`
 * fix: :issue:`27` move track attributes to :class:`Track`
 * fix: :issue:`24` only have "real" tracks in the list(s) (0 not special)
 * fix: :issue:`19` only read the requested features from disc (sparse)
 * fix: :issue:`26` remove :attr:`DiscId.webservice_url` (deprecated)
 * fix: detect the version of libdiscid 0.3.0 also in lib64 installations

Changes in 0.4.0 (2013-04-09):
------------------------------
 * feature: added :data:`FEATURES_IMPLEMENTED`, :attr:`DiscId.track_lengths`,
   :attr:`DiscId.webservice_url` and :attr:`DiscId.freedb_id`
 * feature :issue:`18`: disc access test suite
 * fix :issue:`21`: uninformative error on Windows

Changes in 0.3.0 (2013-03-11):
------------------------------
 * feature :issue:`20`: add :data:`FEATURES` list
 * feature: :func:`DiscId.put`, :attr:`DiscId.track_offsets`,
   :attr:`DiscId.sectors`, :attr:`DiscId.first_track_num`,
   :attr:`DiscId.last_track_num`
 * fix :issue:`17`: test fails on Mac OS X for default_device
 * fix :issue:`16`: prefer libdiscid in current directory
 * fix :issue:`15`: import can now raise :exc:`OSError`
 * fix :issue:`14`: find libdiscid in current folder (Linux/Unix)

Changes in 0.2.1 (2013-01-30):
------------------------------
 * fix :issue:`9`: test fails on Python 3.2 because of unicode literals

Changes in 0.2.0 (2013-01-30):
------------------------------
 * API change from :func:`DiscId.get_id` to :attr:`DiscId.id`
 * added :data:`DEFAULT_DEVICE` as a module constant
 * added :attr:`DiscId.submission_url`
 * added an actual documentation and links to linux packages
 * add tests and continuous integration configuration
 * add changelog

Changes in 0.1.0 (2013-01-12):
------------------------------
 * initial version with :func:`DiscId.read` and :func:`DiscId.get_id`
