discid API
==========

.. automodule:: discid
   :synopsis: Python binding of Libdiscid

At the module level there are these constants available:

.. autodata:: LIBDISCID_VERSION_STRING
   :annotation:

.. autodata:: DEFAULT_DEVICE
   :annotation:

.. autodata:: FEATURES
   :annotation:

.. autodata:: FEATURES_IMPLEMENTED


These functions are used to create a :class:`DiscId` object.

.. autofunction:: read
.. autofunction:: put


DiscId object
-------------

.. autoclass:: DiscId
   :undoc-members:


   .. autoattribute:: id
   .. autoattribute:: freedb_id
   .. autoattribute:: submission_url
   .. autoattribute:: webservice_url
   .. autoattribute:: first_track_num
   .. autoattribute:: last_track_num
   .. autoattribute:: sectors
   .. autoattribute:: track_offsets
   .. autoattribute:: track_lengths
   .. autoattribute:: mcn
   .. autoattribute:: track_isrcs


The discid module includes a custom exception to handle specific problems:

.. autoexception:: DiscError
   :show-inheritance:
