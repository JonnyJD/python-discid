Usage
=====

Basic
-----
The basic use case is::

 # this will load libdiscid
 import discid

 print("device: %s" % discid.DEFAULT_DEVICE)
 disc = discid.read()        # reads from default device
 print("id: %s" % disc.id)
 print("submission url:\n%s" % disc.submission_url)

You can also set the device explicitely::

 device = discid.DEFAULT_DEVICE
 disc = discid.read(device)
 id = disc.id

You can use other devices of course: see :func:`read`.

When anything goes wrong reading from the device, :exc:`DiscError` is raised.

Advanced
--------
Python-discid can do more than just provide the MusicBrainz Disc ID.
You can get details about the tracks an fetch additional features
like the ISRCs and the MCN, which is basically the EAN/UPC of the disc::

 disc = discid.read(features=["mcn", "isrc"])
 print("mcn: %s" % disc.mcn)
 for track in disc.tracks:
     print("{num:>2}: {isrc:13}".format(num=track.number, isrc=track.isrc))

Without Disc Access
-------------------
When you just want to generate disc IDs and you have the necessary data
laying around, you can use :func:`put`.
You will need the numbers of the first track (should be 1),
the number of the last audio track (cut off trailing data tracks),
the total number of sectors for these tracks
and the offset for every one of the tracks up to the last audio track.

An example for the TOC
`TqvKjMu7dMliSfmVEBtrL7sBSno- <http://musicbrainz.org/cdtoc/TqvKjMu7dMliSfmVEBtrL7sBSno->`_::

 first = 1
 last = 15
 offsets = [258725] + [150, 17510, ..., 235590]
 disc = discid.put(first, last, offsets)
 print("id: %s" % disc.id)
 last_track = disc.tracks[disc.last_track_num - 1]
 print("last track length: %s seconds" % last_track.seconds)

.. note:: The example disc has track 16 as a multimedia/data track.
   The sector count for the disc is the ending sector for track 15!
   Depending on how you get this number, you might need to substract
   11400 (2:32 minutes) from your sector count.
   Make sure the last track length is correct!

See also :musicbrainz:`Disc ID Calculation` for details
on which numbers to choose.
