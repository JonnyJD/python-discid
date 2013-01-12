## Libdiscid Python bindings

Python-discid implements Python bindings for MusicBrainz Libdiscid.
This module works with Python &gt;= 2.6, including Python 3.

Libdiscid's main purpose is the calculation of an
identifier of audio discs (disc id)
to use for the MusicBrainz database.

That identifier is calculated from the TOC of the disc,
similar to the freeDB CDDB identifier.
Libdiscid can calculate MusicBranz Disc IDs and 
freeDB Disc IDs.

This module is a very close binding that offloads
all relevant data storage and calculation to Libdiscid.
On the other hand it gives a pythonic API
and uses an object and exceptions.

For more information on Libdiscid see
[libdiscid](http://musicbrainz.org/doc/libdiscid).

For more information about the calculation of these disc ids see
[Disc ID Calculation](http://musicbrainz.org/doc/Disc_ID_Calculation).


### Usage

    # this will load Libdiscid
    from discid import DiscId

    with DiscId() as disc:
        disc.read("/dev/cdrom")
        print "id: %s" % disc.get_id()	# Python 2
        print("id: %s" % disc.get_id())	# Python 3

See also examples.py.

### License

This module is released under the GNU Lesser General Public License Version 3.
See COPYING.LESSER for details.
