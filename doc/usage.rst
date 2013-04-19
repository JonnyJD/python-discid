Usage
=====

Basic
-----

The basic use case is::

 # this will load libdiscid
 import discid

 print("device: %s" % discid.DEFAULT_DEVICE)
 disc = discid.read()        # reads from default device
 print("id: %s" % disc.id)
 print("submission url:\n%s" % disc.submission_url)

You can also set the device explicitely::

 device = discid.DEFAULT_DEVICE
 disc = discid.read(device)
 id = disc.id

You can use other devices of course: see :func:`read`.

When anything goes wrong reading from the device, :exc:`DiscError` is raised.
