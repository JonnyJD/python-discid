discid API
==========

.. automodule:: discid
   :synopsis: Python binding of Libdiscid

Constants
---------
At the module level there are these constants available:

.. autodata:: LIBDISCID_VERSION_STRING
   :annotation:
.. autodata:: FEATURES
   :annotation:
.. autodata:: FEATURES_IMPLEMENTED

Functions
---------
These functions are used to create a :class:`Disc` object.

.. autofunction:: read
.. autofunction:: put

You can get the device that is used as a default with

.. autofunction:: get_default_device

Disc object
-----------
.. autoclass:: Disc
   :undoc-members:

   .. autoattribute:: id
   .. autoattribute:: freedb_id
   .. autoattribute:: submission_url
   .. autoattribute:: toc_string

      .. versionadded:: 1.1

   .. autoattribute:: first_track_num
   .. autoattribute:: last_track_num
   .. autoattribute:: sectors
   .. autoattribute:: length
   .. autoattribute:: seconds
   .. autoattribute:: mcn
   .. autoattribute:: tracks

Track object
------------
.. autoclass:: Track
   :undoc-members:

   .. autoattribute:: number
   .. autoattribute:: offset
   .. autoattribute:: sectors
   .. autoattribute:: length
   .. autoattribute:: seconds
   .. autoattribute:: isrc

Exceptions
----------
The discid module includes a custom exception to handle specific problems:

.. autoexception:: DiscError
   :show-inheritance:
.. autoexception:: TOCError
   :show-inheritance:
