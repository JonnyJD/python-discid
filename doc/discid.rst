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
   :undoc-members:


   You should use :func:`read` before getting
   any data from an object of this class:

   .. automethod:: read


   When the a TOC was successfully read,
   you can access the informational attributes:

   .. autoattribute:: id
   .. autoattribute:: submission_url


   After you are done with the object,
   you should free the memory allocated for it:

   .. automethod:: free


The discid module includes a custom exception to handle specific problems:

.. autoexception:: DiscError
   :show-inheritance:
