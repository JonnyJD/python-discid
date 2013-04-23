#!/usr/bin/env python
# Copyright (C) 2013  Johannes Dewender
# This test is free. You can redistribute and/or modify it at will.

import sys
import unittest

import discid

test_discs = [
        {
            "name": "Guano Apes - Don't give Me Names, without last data track",
            "first": 1,
            "last" : 15,
            "offsets": [258725, 150, 17510, 33275, 45910,
                        57805, 78310, 94650,109580, 132010,
                        149160, 165115, 177710, 203325, 215555, 235590],
            "id": "TqvKjMu7dMliSfmVEBtrL7sBSno-",
            "freedb": "b60d770f"
        }
    ]

class TestModulePrivate(unittest.TestCase):

    # lots of encoding tests, because that is quite different in Python 2/3
    def test_encode(self):
        self.assertTrue(type(discid._encode("test")) is type(b"test"))
        self.assertEqual(discid._encode("test"), b"test")

    def test_decode(self):
        self.assertTrue(type(discid._decode(b"test")) is type(b"test".decode()))
        self.assertEqual(discid._decode(b"test"), "test")

    def test_encoding(self):
        string = "test"
        self.assertEqual(discid._decode(discid._encode(string)), string)
        bytestring = b"test"
        self.assertEqual(discid._encode(discid._decode(bytestring)), bytestring)


class TestModule(unittest.TestCase):

    def test_default_device(self):
        device = discid.DEFAULT_DEVICE
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
        # it will only fail because first > last
        first = 15
        last = 1
        offsets = [258725, 150, 17510, 33275, 45910] # also wrong
        self.assertRaises(discid.DiscError, discid.put, first, last, offsets)

    def test_put_success(self):
        test_disc = test_discs[0]
        disc = discid.put(test_disc["first"], test_disc["last"],
                          test_disc["offsets"])
        self.assertEqual(disc.id, test_disc["id"])
        self.assertEqual(disc.freedb_id, test_disc["freedb"])
        self.assertEqual(disc.first_track_num, test_disc["first"])
        self.assertEqual(disc.last_track_num, test_disc["last"])
        self.assertEqual(disc.track_offsets, test_disc["offsets"])

        # check idempotence (use output again as input)
        first = disc.first_track_num
        last = disc.last_track_num
        offsets = disc.track_offsets
        lengths = disc.track_lengths
        disc = discid.put(first, last, offsets)
        self.assertEqual(disc.id, test_disc["id"])
        self.assertEqual(disc.freedb_id, test_disc["freedb"])
        self.assertEqual(disc.track_offsets, offsets)
        self.assertEqual(disc.first_track_num, first)
        self.assertEqual(disc.last_track_num, last)
        self.assertEqual(disc.track_lengths, lengths)


class TestClass(unittest.TestCase):

    def setUp(self):
        self.disc = discid.DiscId()
        self.assertTrue(self.disc, "No DiscId object created")

    def test_emptyness(self):
        # all should be empty and don't give exceptions
        self.assertTrue(self.disc.id is None)
        self.assertTrue(self.disc.freedb_id is None)
        self.assertTrue(self.disc.submission_url is None)
        self.assertTrue(self.disc.webservice_url is None)
        self.assertTrue(self.disc.mcn is None)
        self.assertFalse(self.disc.first_track_num)
        self.assertFalse(self.disc.last_track_num)
        self.assertFalse(self.disc.sectors)
        self.assertFalse(self.disc.track_isrcs)
        # only test that access doesn't give exceptions
        self.disc.track_offsets
        self.disc.track_lengths

    def tearDown(self):
        self.disc._free()


class TestDisc(unittest.TestCase):
    """Test reading the disc currently in the drive
    """

    def test_default_device(self):
        # Can't be empty, in contrast to the test in TestModule
        device = discid.DEFAULT_DEVICE
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
        self.assertTrue(disc.webservice_url, "Invalid web service url")
        self.assertEqual(disc.sectors, disc.track_offsets[0],
                         "track_offsets[0] must match total sector count")
        num_tracks = len(disc.track_offsets) - 1
        self.assertEqual(disc.last_track_num, num_tracks,
                        "Track number and offset list mismatch")

        for i in range(num_tracks + 1):
            offset = disc.track_offsets[i]
            self.assertTrue(offset <= disc.sectors, "Invalid offset")
            if i > 1:
                previous_offset = disc.track_offsets[i-1]
                self.assertTrue(offset >= previous_offset,
                                "Invalid offset list")

        # additional features should be unset, not empty
        self.assertTrue(disc.mcn is None)

        # check idempotence (use output again as input to put)
        disc_id = disc.id
        freedb_id = disc.freedb_id
        submission_url = disc.submission_url
        webservice_url = disc.webservice_url
        first = disc.first_track_num
        offsets = disc.track_offsets
        lengths = disc.track_lengths
        disc = discid.put(first, num_tracks, offsets)
        self.assertEqual(disc.id, disc_id, "different id after put")
        self.assertEqual(disc.freedb_id, freedb_id,
                         "different freedb id after put")
        self.assertEqual(disc.track_offsets, offsets,
                         "different offsets after put")
        self.assertEqual(disc.submission_url, submission_url,
                         "different submission_url after put")
        self.assertEqual(disc.webservice_url, webservice_url,
                         "different webservice_url after put")
        self.assertEqual(disc.first_track_num, first,
                         "different first track after put")
        self.assertEqual(disc.last_track_num, num_tracks,
                         "different last track after put")
        self.assertEqual(disc.sectors, offsets[0],
                         "different sector count after put")
        self.assertEqual(disc.track_lengths, lengths,
                         "different lengths after put")

    def test_read_features(self):
        disc = discid.read(features=["mcn", "isrc"]) # read from default drive
        self.assertEqual(len(disc.id), 28, "Invalid Disc ID")
        self.assertTrue(disc.submission_url, "Invalid submission url")

        if "mcn" in discid.FEATURES:
            self.assertTrue(disc.mcn is not None)
        else:
            self.assertTrue(disc.mcn is None)

        if "isrc" in discid.FEATURES:
            self.assertTrue(disc.track_isrcs)
        else:
            self.assertFalse(disc.track_isrcs)

    def test_read_put(self):
        # a read followed with a put, which should clear the features
        disc = discid.read(features=["mcn", "isrc"]) # read from default drive
        test_disc = test_discs[0]
        disc = discid.put(test_disc["first"], test_disc["last"],
                          test_disc["offsets"])
        self.assertTrue(disc.mcn is None)
        self.assertFalse(disc.track_isrcs)


if __name__ == "__main__":
    unittest.main()


# vim:set shiftwidth=4 smarttab expandtab:
