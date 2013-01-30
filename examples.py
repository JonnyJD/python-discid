#!/usr/bin/env python
# Copyright (C) 2013  Johannes Dewender
# This example is free. You can redistribute and/or modify it at will.

# this will load Libdiscid
import discid

def recommended_example():
    with discid.DiscId() as disc:
        disc.read()       # use default device
        print("id: %s" % disc.id)
        print("used %s as device" % discid.DEFAULT_DEVICE)
        print("submit with:\n%s" % disc.submission_url)

def other_example():
    disc = discid.DiscId()
    device = discid.DEFAULT_DEVICE
    disc.read("/dev/cdrom")
    #print "id: %s" % disc.id # Python 2
    print("id: %s" % disc.id) # Python 3
    disc.free()

recommended_example()
#other_example()

# vim:set shiftwidth=4 smarttab expandtab:
