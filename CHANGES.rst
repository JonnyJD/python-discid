Changelog
=========

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
