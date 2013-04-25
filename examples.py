#!/usr/bin/env python
# Copyright (C) 2013  Johannes Dewender
# This example is free. You can redistribute and/or modify it at will.

# this will load Libdiscid
import discid

SECTORS_PER_SECOND = 75

def simple_example():
    disc = discid.read()       # use default device
    print("id: %s" % disc.id)
    print("used %s as device" % discid.DEFAULT_DEVICE)
    print("submit with:\n%s" % disc.submission_url)

def complex_example():
    disc = discid.read("/dev/cdrom", ["mcn", "isrc"])
    print("id:  %s" % disc.id)
    print("MCN: %s" % disc.mcn)
    for track in disc.tracks:
        seconds = track.length // SECTORS_PER_SECOND
        length = "{min:>2.0f}:{sec:>02.0f} ({sectors:>6})".format(
                min=(seconds // 60), sec=(seconds % 60), sectors=track.length)
        print("{num:>2}: {offset:>6} {len}\tISRC: {isrc:13}".format(
            num=track.number, offset=track.offset, len=length, isrc=track.isrc))

simple_example()
#complex_example()

# vim:set shiftwidth=4 smarttab expandtab:
