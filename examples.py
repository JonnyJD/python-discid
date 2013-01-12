#!/usr/bin/env python
# Copyright (C) 2013  Johannes Dewender
# This example is free. You can redistribute and/or modify it at will.

import discid

device = "/dev/cdrom" 

def recommended_example():
    with discid.DiscId() as disc:
        disc.read(device)
        #print "id: %s" % disc.get_id() # Python 2
        print("id: %s" % disc.get_id()) # Python 3

def other_example():
    disc = discid.DiscId()
    disc.read(device)
    #print "id: %s" % disc.get_id() # Python 2
    print("id: %s" % disc.get_id()) # Python 3
    disc.free()

recommended_example()
#other_example()

# vim:set shiftwidth=4 smarttab expandtab:
