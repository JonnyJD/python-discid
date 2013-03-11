#!/usr/bin/env python
# Copyright (C) 2013  Johannes Dewender
# This test is free. You can redistribute and/or modify it at will.

import sys
import unittest

import discid

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


class TestClass(unittest.TestCase):

    def setUp(self):
        self.disc = discid.DiscId()
        self.assertTrue(self.disc, "No DiscId object created")

    def test_invalid_device(self):
        device = "non_existing_device"
        self.assertRaises(discid.DiscError, self.disc.read, device)

    def test_device_encoding(self):
        device = b"non_existing_device".decode()
        self.assertRaises(discid.DiscError, self.disc.read, device)
        devicebytes = b"non_existing_device"
        self.assertRaises(discid.DiscError, self.disc.read, devicebytes)

    def test_empty_id(self):
        self.assertTrue(self.disc.id is None)

    def test_empty_submission_url(self):
        self.assertTrue(self.disc.submission_url is None)

    def test_put_fail(self):
        # it will only fail because first > last
        first = 15
        last = 1
        offsets = [258725, 150, 17510, 33275, 45910] # also wrong
        self.assertRaises(discid.DiscError, self.disc.put, first, last, offsets)

    def test_put_success(self):
        first = 1
        last = 15
        offsets = [258725, 150, 17510, 33275, 45910,
                   57805, 78310, 94650,109580, 132010,
                   149160, 165115, 177710, 203325, 215555, 235590]
        # Guano Apes - Don't give Me Names, without the last data track
        disc_id = "TqvKjMu7dMliSfmVEBtrL7sBSno-"
        self.disc.put(first, last, offsets)
        self.assertEquals(self.disc.id, disc_id)

        # check idempotence (use output again as input)
        first = self.disc.first_track_num
        last = self.disc.last_track_num
        offsets = self.disc.track_offsets
        self.disc.put(first, last, offsets)
        self.assertEquals(self.disc.id, disc_id)

    def tearDown(self):
        self.disc.free()


if __name__ == "__main__":
    unittest.main()


# vim:set shiftwidth=4 smarttab expandtab:
