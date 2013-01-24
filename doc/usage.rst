Usage
=====

Basic
-----

It is recommended to use :class:`DiscId <discid.DiscId>` like this::

 # this will load libdiscid
 import discid

 with discid.DiscId() as disc:
     print("device: %s" % disc.DEFAULT_DEVICE)
     disc.read()        # reads from default device
     print("id: %s" % disc.id)

This will make sure the internal object is removed afterwards.

If you don't use *with*,
then you have to use :func:`DiscId.free <discid.DiscId.free>`::

 disc = discid.DiscId()
 device = discid.DEFAULT_DEVICE()
 disc.read(device)
 id = disc.id
 disc.free()
 # disc can't be used anymore

You can use other devices of course:
see :func:`DiscId.read <discid.DiscId.read>`.

When anything goes wrong reading from the device,
:exc:`DiscError <discid.DiscError>` is raised.
