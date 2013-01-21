#!/usr/bin/env python
# Copyright (C) 2013  Johannes Dewender
# This test is free. You can redistribute and/or modify it at will.

import sys
import unittest

import discid


class TestModule(unittest.TestCase):

    def test_default_device(self):
        device = discid.DEFAULT_DEVICE
        self.assertTrue(device, "No default device given")


class TestClass(unittest.TestCase):

    def setUp(self):
        self.disc = discid.DiscId()
        self.assertTrue(self.disc, "No DiscId object created")

    def runTest(self):
        pass

    def tearDown(self):
        self.disc.free()


if __name__ == "__main__":
    unittest.main()


# vim:set shiftwidth=4 smarttab expandtab:
