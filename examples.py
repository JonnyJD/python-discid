#!/usr/bin/python2

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
