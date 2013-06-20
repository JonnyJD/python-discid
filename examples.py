#!/usr/bin/env python
# Copyright (C) 2013  Johannes Dewender
# This example is free. You can redistribute and/or modify it at will.

# this will load Libdiscid
import discid

def simple_example():
    disc = discid.read()       # use default device
    print("id: %s" % disc.id)
    print("used %s as device" % discid.get_default_device())
    print("submit with:\n%s" % disc.submission_url)


def _length_str(seconds, sectors):
    return "{min:>2.0f}:{sec:>02.0f} ({sectors:>6})".format(
        min=(seconds // 60), sec=(seconds % 60), sectors=sectors)

def complex_example():
    disc = discid.read("/dev/cdrom", ["mcn", "isrc"])
    print("id:\t%s" % disc.id)
    print("MCN:\t%s" % disc.mcn)
    print("length:\t%s" % _length_str(disc.seconds, disc.sectors))
    for track in disc.tracks:
        length = _length_str(track.seconds, track.sectors)
        print("{num:>2}: {offset:>6} {len}\tISRC: {isrc:13}".format(
            num=track.number, offset=track.offset, len=length, isrc=track.isrc))

if __name__ == "__main__":
    simple_example()
    #complex_example()

# vim:set shiftwidth=4 smarttab expandtab:
