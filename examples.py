#!/usr/bin/python2
# Copyright (C) 2013  Johannes Dewender
# This example is free. You can redistribute and/or modify it at will.

import discid

device = "/dev/cdrom" 

def recommended_example():
    with discid.DiscId() as disc:
        disc.read(device)
        print disc.get_id()

def other_example():
    disc = discid.DiscId()
    disc.read(device)
    print disc.get_id()
    disc.free()

recommended_example()
#other_example()

# vim:set shiftwidth=4 smarttab expandtab:
