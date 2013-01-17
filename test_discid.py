#!/usr/bin/env python
# Copyright (C) 2013  Johannes Dewender
# This test is free. You can redistribute and/or modify it at will.

import sys
import discid

device = discid.get_default_device()
print("default device: %s" % device)
if device is None or len(device) == 0:
    sys.exit("error: device not set")

disc = discid.DiscId()
if disc is None:
    sys.exit("error: disc object not created")

disc.free()

print("All tests successfull")


# vim:set shiftwidth=4 smarttab expandtab:
