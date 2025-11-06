.. index:: Schema Link Header

.. Copyright © 2025 David Charboneau
..    This work is licensed under Creative Commons Attribution 4.0 International
..    https://creativecommons.org/licenses/by/4.0/


.. _Schema Link Header:

******************
Schema Link Header
******************

A conforming :ref:`Semantic HTTP Resource` **MUST** provide a ``link`` header
for any HTTP response that returns an entity body specifying a schema resource.
The ``link`` header **MUST** include a ``rel`` attribute with the value of
``describedBy`` or recognized equivalent. There is no recognized equivalent
value for the ``rel`` attribute in this revision of the standard.

Example
=======

An XML resource format may be defined or described by an XML schema. A *Schema
Link Header* for the XML schema would look like:

.. sourcecode:: http

   link: <http://example.com/schemas/user.xml>;
         rel="describedBy";
         type="application/xml"

