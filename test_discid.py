#!/usr/bin/env python
# Copyright (C) 2013  Johannes Dewender
# This test is free. You can redistribute and/or modify it at will.

import sys
import math
import unittest

import discid

test_discs = [
        {
            "name": "Guano Apes - Don't give Me Names, without last data track",
            "first": 1,
            "last" : 15,
            "sectors": 258725,
            "offsets": [150, 17510, 33275, 45910,
                        57805, 78310, 94650,109580, 132010,
                        149160, 165115, 177710, 203325, 215555, 235590],
            "id": "TqvKjMu7dMliSfmVEBtrL7sBSno-",
            "freedb": "b60d770f"
        }
    ]

class TestModulePrivate(unittest.TestCase):

    # lots of encoding tests
    # not part of the actual API, but this is quite different in Python 2/3
    def test_encode(self):
        self.assertTrue(type(discid.util._encode("test")) is type(b"test"))
        self.assertEqual(discid.util._encode("test"), b"test")

    def test_decode(self):
        self.assertTrue(type(discid.util._decode(b"test"))
                        is type(b"test".decode()))
        self.assertEqual(discid.util._decode(b"test"), "test")

    def test_encoding(self):
        string = "test"
        self.assertEqual(discid.util._decode(discid.util._encode(string)),
                         string)
        bytestring = b"test"
        self.assertEqual(discid.util._encode(discid.util._decode(bytestring)),
                         bytestring)


class TestModule(unittest.TestCase):

    def test_version_string(self):
        version_string = discid.LIBDISCID_VERSION_STRING
        self.assertTrue(version_string is not None, "No version string given")

    def test_default_device(self):
        device = discid.get_default_device()
        self.assertTrue(device is not None, "No default device given")

    def test_features(self):
        features = discid.FEATURES
        self.assertTrue(features is not None, "No feature list given")

    def test_features_implemented(self):
        features = discid.FEATURES_IMPLEMENTED
        self.assertTrue(features, "No feature list implemented")

    def test_invalid_device(self):
        device = "non_existing_device"
        self.assertRaises(discid.DiscError, discid.read, device)

    def test_device_encoding(self):
        device = b"non_existing_device".decode()
        self.assertRaises(discid.DiscError, discid.read, device)
        devicebytes = b"non_existing_device"
        self.assertRaises(discid.DiscError, discid.read, devicebytes)

    def test_put_fail(self):
        # not enough offsets
        self.assertRaises(discid.TOCError, discid.put, 1, 2, 150, [150])
        # too many offsets
        self.assertRaises(discid.TOCError,
                          discid.put, 1, 2, 1000, [150, 500, 750])
        # total sectors / offset mismatch
        self.assertRaises(discid.TOCError, discid.put, 1, 2, 150, [150, 500])

    def test_put_success(self):
        test_disc = test_discs[0]
        disc = discid.put(test_disc["first"], test_disc["last"],
                          test_disc["sectors"], test_disc["offsets"])
        self.assertEqual(disc.id, test_disc["id"])
        self.assertEqual(disc.freedb_id, test_disc["freedb"])
        self.assertEqual(disc.first_track_num, test_disc["first"])
        self.assertEqual(disc.last_track_num, test_disc["last"])
        self.assertEqual(disc.sectors, test_disc["sectors"])
        track_offsets = [track.offset for track in disc.tracks]
        self.assertEqual(track_offsets, test_disc["offsets"])
        self.assertEqual(disc.sectors,
                         disc.tracks[-1].offset + disc.tracks[-1].sectors)
        self.assertEqual(disc.seconds, math.floor((disc.sectors / 75.0) + 0.5))
        self.assertEqual(type(disc.seconds), int)
        for track in disc.tracks:
            self.assertEqual(track.seconds,
                             math.floor((track.sectors / 75.0) + 0.5))
            self.assertEqual(type(track.seconds), int)
        toc_string = ["1", disc.last_track_num, disc.sectors] + track_offsets
        toc_string = " ".join(map(str, toc_string))
        self.assertEqual(disc.toc_string, toc_string)


class TestDisc(unittest.TestCase):
    """Test reading the disc currently in the drive
    """

    def test_default_device(self):
        # Can't be empty, in contrast to the test in TestModule
        device = discid.get_default_device()
        self.assertTrue(device, "No default device given")

    def test_features(self):
        # Can't be empty, in contrast to the test in TestModule
        features = discid.FEATURES
        self.assertTrue(features, "No feature list given")

    def test_read_simple(self):
        disc = discid.read()        # read from default drive
        self.assertEqual(len(disc.id), 28, "Invalid Disc ID")
        self.assertEqual(len(disc.freedb_id), 8, "Invalid FreeDB Disc ID")
        self.assertTrue(disc.submission_url, "Invalid submission url")
        self.assertTrue(disc.toc_string, "Invalid toc string")
        self.assertEqual(disc.last_track_num, len(disc.tracks),
                        "Wrong amount of tracks")
        self.assertEqual(disc.sectors,
                         disc.tracks[-1].offset + disc.tracks[-1].sectors)

        for track in disc.tracks:
            self.assertTrue(track.offset <= disc.sectors, "Invalid offset")
            if track.number > 1:
                previous_offset = disc.tracks[track.number-2].offset
                self.assertTrue(track.offset >= previous_offset,
                                "Invalid offset series")

        # additional features should be unset, not empty
        self.assertTrue(disc.mcn is None)
        for track in disc.tracks:
            self.assertTrue(track.isrc is None)

        # check idempotence (use output again as input to put)
        disc_id = disc.id
        freedb_id = disc.freedb_id
        submission_url = disc.submission_url
        toc_string = disc.toc_string
        first = disc.first_track_num
        last = disc.last_track_num
        sectors = disc.sectors
        track_sectors = [track.sectors for track in disc.tracks]
        track_offsets = [track.offset for track in disc.tracks]

        disc = discid.put(first, last, sectors, track_offsets)
        self.assertEqual(disc.id, disc_id, "different id after put")
        self.assertEqual(disc.freedb_id, freedb_id,
                         "different freedb id after put")
        self.assertEqual(disc.submission_url, submission_url,
                         "different submission_url after put")
        self.assertEqual(disc.toc_string, toc_string,
                         "different toc_string after put")
        self.assertEqual(disc.first_track_num, first,
                         "different first track after put")
        self.assertEqual(disc.last_track_num, last,
                         "different last track after put")
        self.assertEqual(disc.sectors, sectors,
                         "different sector count after put")
        new_offsets = [track.offset for track in disc.tracks]
        self.assertEqual(new_offsets, track_offsets,
                         "different offsets after put")
        new_sectors = [track.sectors for track in disc.tracks]
        self.assertEqual(new_sectors, track_sectors,
                         "different lengths after put")

    def test_read_features(self):
        disc = discid.read(features=["mcn", "isrc"]) # read from default drive
        self.assertEqual(len(disc.id), 28, "Invalid Disc ID")
        self.assertTrue(disc.submission_url, "Invalid submission url")
        self.assertTrue(disc.toc_string, "Invalid toc string")

        if "mcn" in discid.FEATURES:
            self.assertTrue(disc.mcn is not None)
        else:
            self.assertTrue(disc.mcn is None)

        for track in disc.tracks:
            if "isrc" in discid.FEATURES:
                self.assertTrue(track.isrc is not None)
            else:
                self.assertTrue(track.isrc is None)

    def test_read_put(self):
        # a read followed with a put, which should clear the features
        disc = discid.read(features=["mcn", "isrc"]) # read from default drive
        test_disc = test_discs[0]
        disc = discid.put(test_disc["first"], test_disc["last"],
                          test_disc["sectors"], test_disc["offsets"])
        self.assertTrue(disc.mcn is None)
        for track in disc.tracks:
            self.assertTrue(track.isrc is None)


if __name__ == "__main__":
    unittest.main()


# vim:set shiftwidth=4 smarttab expandtab:
