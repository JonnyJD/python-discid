#!/usr/bin/env python
# Copyright (C) 2013  Johannes Dewender
# This example is free. You can redistribute and/or modify it at will.

# this will load Libdiscid
import discid

def simple_example():
    disc = discid.read()       # use default device
    print("id: %s" % disc.id)
    print("used %s as device" % discid.DEFAULT_DEVICE)
    print("submit with:\n%s" % disc.submission_url)

def feature_example():
    disc = discid.read("/dev/cdrom", ["mcn"])
    print("id:  %s" % disc.id)
    print("MCN: %s" % disc.mcn)

simple_example()
#feature_example()

# vim:set shiftwidth=4 smarttab expandtab:
