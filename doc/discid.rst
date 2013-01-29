discid API
==========

.. automodule:: discid
   :synopsis: Python binding of Libdiscid

At the module level there is one constant available:

.. autodata:: DEFAULT_DEVICE
   :novalue:


DiscId object
-------------

The user is expected to create a :class:`DiscId` object,
feed it with some type of TOC and extract the generated information.

.. autoclass:: DiscId
   :members:
   :undoc-members:

.. autoexception:: DiscError
   :show-inheritance:
